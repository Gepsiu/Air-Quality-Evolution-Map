from django.db import models


class Measurement(models.Model):
    id = models.IntegerField(primary_key=True)
    pollutant = models.CharField(max_length=20)
    measurement_date = models.DateField()
    station = models.CharField(max_length=30)
    measurement_value = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = "measurements"
