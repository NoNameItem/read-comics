from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count, F, Max, Q
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from read_comics.story_arcs.models import StoryArc
from read_comics.utils import logging
from read_comics.utils.fields import ThumbnailImageField
from read_comics.volumes.models import Volume

logger = logging.getLogger(__name__)


def get_user_image_name(instance, filename):
    return f"user_image/{instance.username}_logo.{filename.split('.')[-1]}"


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")
        UNICORN = "U", _("Unicorn")
        OTHER = "O", _("Other")

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Full name"), blank=True, max_length=255)
    gender = models.CharField(_("Gender"), max_length=1, choices=Gender.choices, default=Gender.UNICORN)
    _user_image = ThumbnailImageField(null=True, upload_to=get_user_image_name, thumb_width=40)
    bio = models.CharField(_("Bio"), blank=True, max_length=1000)
    birth_date = models.DateField(_("Birth date"), null=True, blank=True)
    show_email = models.BooleanField(_("Show email in profile"), default=False)
    last_active = models.DateTimeField(_("Last active"), null=True)
    unlimited_downloads = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def image_url(self):
        if self._user_image:
            return self._user_image.url
        else:
            return f"/static/images/avatars/{self.gender}.png"

    @property
    def image_thumb_url(self):
        if self._user_image:
            return self._user_image.thumb_url
        else:
            return f"/static/images/avatars/{self.gender}_thumb.png"

    def __str__(self):
        return self.name or self.username.title()

    @logging.logged(logger)
    def save(self, *args, **kwargs):
        if not self.name:
            if self.first_name and self.last_name:
                self.name = f"{self.first_name} {self.last_name}"
            elif self.first_name:
                self.name = self.first_name
            elif self.last_name:
                self.name = self.last_name
        super(User, self).save(*args, **kwargs)

    def get_started_and_not_finished(self, model):
        return (
            model.objects.was_matched()
            .annotate(issue_count=Count("issues", distinct=True))
            .select_related("publisher")
            .annotate(
                finished_count=Count("issues", filter=Q(issues__finished_users=self)),
                max_finished_date=Max("issues__finished__finish_date", filter=Q(issues__finished__user=self)),
            )
            .filter(finished_count__gte=1)
            .exclude(finished_count=F("issue_count"))
            .order_by("-max_finished_date")
        )

    @property
    def started_and_not_finished_volumes(self):
        return self.get_started_and_not_finished(Volume)

    @property
    def started_and_not_finished_story_arcs(self):
        return self.get_started_and_not_finished(StoryArc)
