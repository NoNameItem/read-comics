from django.core.management.base import BaseCommand

from ...models import APIQueue


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("endpoints", nargs="+", type=str)

    def handle(self, *args, **options):
        if len(options["endpoints"]) == 0:
            APIQueue.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Cleared all queues"))
            return

        for endpoint in options["endpoints"]:
            APIQueue.objects.filter(endpoints=endpoint).delete()
            self.stdout.write(self.style.SUCCESS(f"Cleared {endpoint} queue"))
