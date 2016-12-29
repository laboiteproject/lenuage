from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from .views import AppBusUpdateView, AppBusCreateView, AppBusDeleteView, BusStopAutocomplete

urlpatterns = [
    url(r"^create/$", login_required(AppBusCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppBusUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppBusDeleteView.as_view()), name="delete"),
    url(r"^stop-autocomplete/$", BusStopAutocomplete.as_view(), name="stop-autocomplete"),
]
