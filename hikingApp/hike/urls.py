from django.urls import path
from . import views

urlpatterns = [
    path("routeplanner/", views.routeplanner, name="routeplanner"),
    path("", views.frontpage, name="frontpage")
    ]