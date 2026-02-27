from django.shortcuts import render


def main(request):
    return render(request, 'map/map.html', context={})
