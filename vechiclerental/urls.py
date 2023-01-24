from api import views as api_views
from django.urls import path
from rest_framework import permissions

urlpatterns = [
    path("admin_login/", api_views.admin_login),
    path("admin_vehicle_station/", api_views.admin_vehicle_station),
    path("admin_vehicle/", api_views.admin_vehicle),
    path("user_signup/", api_views.user_signup),
    path("user_login/", api_views.user_login),
    path("user_vehicle_station/", api_views.user_vehicle_station),
    path("user_vehicle/", api_views.user_vehicle),
]
