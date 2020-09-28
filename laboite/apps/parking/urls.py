from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppParkingCreateView, AppParkingUpdateView, AppParkingDeleteView

app_name = "laboite"

urlpatterns = [
    path("create/", login_required(AppParkingCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppParkingUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppParkingDeleteView.as_view()), name="delete"),
]
