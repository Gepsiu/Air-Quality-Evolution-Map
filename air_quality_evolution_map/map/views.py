import json

from django.shortcuts import render

from .models import Measurement


def main(request):
    with open('static/geo/wojewodztwa-max.geojson') as file:
        geojson = json.load(file)
    pollution = Measurement.objects.values_list("pollutant", flat=True).distinct()
    pollution_left = [pollution[pollutant] for pollutant in range(0, len(pollution), 3)]
    pollution_middle = [pollution[pollutant] for pollutant in range(1, len(pollution), 3)]
    pollution_right = [pollution[pollutant] for pollutant in range(2, len(pollution), 3)]

    years = [d.year for d in Measurement.objects.dates('measurement_date', 'year')]
    return render(request, 'map/map.html',
                  context={"geojson": geojson,
                           "pollution": {"left": pollution_left, "middle": pollution_middle, "right": pollution_right},
                           "years": years})
