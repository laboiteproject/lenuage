from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from .views import AppEnergyUpdateView, AppEnergyCreateView, AppEnergyDeleteView

urlpatterns = [
    url(r"^create/$", login_required(AppEnergyCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppEnergyUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppEnergyDeleteView.as_view()), name="delete"),
]
