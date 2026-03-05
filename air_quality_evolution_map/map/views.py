import json

from django.shortcuts import render


def main(request):
    with open('static/geo/wojewodztwa-max.geojson') as file:
        geojson = json.load(file)
    return render(request, 'map/map.html', context={"geojson": geojson})
