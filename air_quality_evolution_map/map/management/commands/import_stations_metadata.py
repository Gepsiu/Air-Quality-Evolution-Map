from django.core.management.base import BaseCommand

from map.scripts import stations_metadata_loader


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Script started..."))
        try:
            stations_metadata_loader.main()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"ERROR: {e}"))
        self.stdout.write(self.style.SUCCESS("Finished importing stations metadata"))
