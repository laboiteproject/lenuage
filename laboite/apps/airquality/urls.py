from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AppAirQualityCreateView, AppAirQualityUpdateView, AppAirQualityDeleteView


urlpatterns = [
    url(r"^create/$", login_required(AppAirQualityCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppAirQualityUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppAirQualityDeleteView.as_view()), name="delete"),
]
