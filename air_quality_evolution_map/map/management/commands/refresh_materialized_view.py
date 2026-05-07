from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Script started..."))
        with connection.cursor() as cursor:
            cursor.execute("REFRESH MATERIALIZED VIEW measurement_agg;")
        self.stdout.write(self.style.SUCCESS("Finished!"))
