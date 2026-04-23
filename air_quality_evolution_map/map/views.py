import json
from datetime import date
from pathlib import Path

from django.http import JsonResponse
from django.shortcuts import render

from .models import Measurement, MeasurementAgg

PROJECT_PATH = Path(__file__).resolve().parent.parent


def load_coord(path: str):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Brak pliku: {path}")
    except json.JSONDecodeError:
        raise RuntimeError(f"Błąd JSON w pliku: {path}")


def main(request):
    geojson = load_coord(f'{PROJECT_PATH}\static\geo\wojewodztwa-max.geojson')
    coord_provinces = load_coord(f'{PROJECT_PATH}\static\geo\coord_provinces.json')
    legend = load_coord(f'{PROJECT_PATH}\static\legend\legend.json')
    pollution = Measurement.objects.values_list("pollutant", flat=True).distinct()
    pollution_left = [pollution[pollutant] for pollutant in range(0, len(pollution), 3)]
    pollution_middle = [pollution[pollutant] for pollutant in range(1, len(pollution), 3)]
    pollution_right = [pollution[pollutant] for pollutant in range(2, len(pollution), 3)]
    years = [d.year for d in Measurement.objects.dates('measurement_date', 'year')]

    return render(request, 'map/map.html',
                  context={"geojson": geojson,
                           "pollution": {"left": pollution_left, "middle": pollution_middle, "right": pollution_right},
                           'coord_provinces': coord_provinces, "pollution_scale": legend,
                           "years": years})


def map_data(request):
    pollutant = request.GET.get("pollutant")
    year = request.GET.get("year")
    month = request.GET.get("month")

    if not (pollutant and year and month):
        return JsonResponse({}, status=400)

    start_date = date(int(year), int(month), 1)

    qs = MeasurementAgg.objects.filter(
        pollutant=pollutant,
        start_date=start_date,
    ).values("voivodeship", "avg_value")

    data = {item["voivodeship"]: float(item["avg_value"]) for item in qs}
    print(data, pollutant, start_date)
    return JsonResponse(data)
