from django.core.management.base import BaseCommand

from map.scripts import pollution_data_loader


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Script started..."))
        try:
            pollution_data_loader.main()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
        self.stdout.write(self.style.SUCCESS("Finished importing pollution data"))
