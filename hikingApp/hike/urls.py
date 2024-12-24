from django.urls import path
from . import views

urlpatterns = [
    path("routeplanner/", views.routeplanner, name="routeplanner"),
    path("", views.frontpage, name="frontpage"),
    path("login/", views.login, name="login"),
    path('api/coordinates/', views.receive_coordinates, name='receive_coordinates'),
    ]