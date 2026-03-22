from django.core.management.base import BaseCommand

from map.scripts import file_converter_to_df


class Command(BaseCommand):

    def handle(self, *args, **options):
        file_converter_to_df.main()
        self.stdout.write(self.style.SUCCESS("Finished importing pollution data"))
