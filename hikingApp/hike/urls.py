from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="routeplanner"),
    path("map/", views.map, name="map")
    ]