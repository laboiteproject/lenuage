from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppAirQualityCreateView, AppAirQualityUpdateView, AppAirQualityDeleteView


urlpatterns = [
    path("create/", login_required(AppAirQualityCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppAirQualityUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppAirQualityDeleteView.as_view()), name="delete"),
]
