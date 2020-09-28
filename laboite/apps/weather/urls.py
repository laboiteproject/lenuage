from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppWeatherUpdateView, AppWeatherCreateView, AppWeatherDeleteView

app_name = "laboite"

urlpatterns = [
    path("create/", login_required(AppWeatherCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppWeatherUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppWeatherDeleteView.as_view()), name="delete"),
]
