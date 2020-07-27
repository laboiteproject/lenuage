from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppEnergyUpdateView, AppEnergyCreateView, AppEnergyDeleteView

app_name = "laboite"

urlpatterns = [
    path("create/", login_required(AppEnergyCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppEnergyUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppEnergyDeleteView.as_view()), name="delete"),
]
