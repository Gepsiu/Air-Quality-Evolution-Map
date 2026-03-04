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


class MonthlyMeasurement(models.Model):
    id = models.IntegerField(db_column="month_id", primary_key=True)
    station = models.CharField(db_column="station", max_length=30)
    pollutant = models.CharField(db_column="pollutant", max_length=20)
    month_start = models.DateField(db_column="month_start")
    avg_value = models.DecimalField(db_column="avg_value", max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = "monthly_measurement"


class YearlyMeasurement(models.Model):
    id = models.IntegerField(db_column="year_id", primary_key=True)
    station = models.CharField(db_column="station", max_length=30)
    pollutant = models.CharField(db_column="pollutant", max_length=20)
    year_start = models.DateField(db_column="year_start")
    avg_value = models.DecimalField(db_column="avg_value", max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = "yearly_measurement"
