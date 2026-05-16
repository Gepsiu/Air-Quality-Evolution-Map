from django.urls import path

from . import views

app_name = 'map'

urlpatterns = [
    path('', views.main, name='map'),
    path('data/', views.map_data, name='map_data'),
]
