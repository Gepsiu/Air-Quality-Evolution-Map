from django.db import models


class Station(models.Model):
    code = models.CharField(max_length=40, primary_key=True)
    outdated_code = models.CharField(max_length=40, blank=True, null=True)
    voivodeship = models.CharField(max_length=20)

    def __str__(self):
        return self.code

    class Meta:
        db_table = "stations"


class Measurement(models.Model):
    pollutant = models.CharField(max_length=20)
    measurement_date = models.DateField()
    station = models.ForeignKey(Station, on_delete=models.PROTECT, db_column="station")
    measurement_value = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "measurements"


class MeasurementAgg(models.Model):
    id = models.IntegerField(db_column="id", primary_key=True)
    voivodeship = models.CharField(db_column="station", max_length=20)
    pollutant = models.CharField(db_column="pollutant", max_length=20)
    start_date = models.DateField(db_column="start_date")
    avg_value = models.DecimalField(db_column="avg_value", max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = "measurement_agg"
