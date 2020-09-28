from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppWifiCreateView, AppWifiUpdateView, AppWifiDeleteView

app_name = "laboite"

urlpatterns = [
    path("create/", login_required(AppWifiCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppWifiUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppWifiDeleteView.as_view()), name="delete"),
]
