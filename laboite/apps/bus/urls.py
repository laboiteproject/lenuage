from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppBusUpdateView, AppBusCreateView, AppBusDeleteView, BusStopAutocomplete

urlpatterns = [
    path("create/", login_required(AppBusCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppBusUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppBusDeleteView.as_view()), name="delete"),
    path("stop-autocomplete/", BusStopAutocomplete.as_view(), name="stop-autocomplete"),
]
