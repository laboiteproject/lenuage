from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AppWifiCreateView, AppWifiUpdateView, AppWifiDeleteView


urlpatterns = [
    url(r"^create/$", login_required(AppWifiCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppWifiUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppWifiDeleteView.as_view()), name="delete"),
]
