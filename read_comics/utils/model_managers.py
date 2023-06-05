from django.db import IntegrityError, models
from django.db.models.manager import BaseManager

from . import logging

logger = logging.getLogger(__name__)


class ComicvineSyncQuerySet(models.QuerySet):
    def get_or_create_from_comicvine(
        self, comicvine_id, defaults=None, force_refresh=False, follow_m2m=True, delay=False
    ):
        """
        Creates instance with specified comicvine_id and tries to populate fields with information from comicvine dump.

        Method placed in custom QuerySet like get_or_create method and to get access to get_or_create
        :param comicvine_id: Object's comicvine id
        :param defaults: default fields to pass in standard django get_or_create method
        :param force_refresh: by default only new instances populated with data from comicvine. Set this param to `True`
        to force refresh of already existing instance
        :param follow_m2m: Flag to follow m2m relations while filling info from comicvine
        :param delay: Send task to celery instead of running in this tread
        :return: tuple of 3 elements:
            * found or created instance
            * created flag as in get_or_create
            * comicvine matched flag
        """
        if defaults is None:
            defaults = {}
        defaults["name"] = defaults.get("name", str(comicvine_id))
        try:
            instance, created = self.get_or_create(comicvine_id=comicvine_id, defaults=defaults)
        except IntegrityError:
            instance = self.get(comicvine_id=comicvine_id)
            created = False
        logger.debug(f"Found: {not created}")
        if (created or (force_refresh and not instance.comicvine_actual)) and (
            instance.comicvine_status != instance.ComicvineStatus.QUEUED
        ):
            logger.debug("Refreshing from comicvine")
            instance.fill_from_comicvine(follow_m2m, delay)
            instance.save()
        return instance, created, (instance.comicvine_status == instance.ComicvineStatus.MATCHED)

    def matched(self):
        return self.filter(comicvine_status=self.model.ComicvineStatus.MATCHED)

    def not_matched(self):
        return self.filter(comicvine_status=self.model.ComicvineStatus.NOT_MATCHED)

    def queued(self):
        return self.filter(comicvine_status=self.model.ComicvineStatus.QUEUED)

    def was_matched(self):
        return self.filter(comicvine_last_match__isnull=False)


# pylint: disable-next=R0903
class ComicvineSyncManager(BaseManager.from_queryset(ComicvineSyncQuerySet)):  # type: ignore[misc]
    pass
