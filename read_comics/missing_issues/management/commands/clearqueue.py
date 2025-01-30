from django.core.management.base import BaseCommand

from ...models import APIQueue


class Command(BaseCommand):
    def handle(self, *args, **options):
        APIQueue.objects.all().delete()
