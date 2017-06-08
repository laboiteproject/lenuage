from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AppParkingCreateView, AppParkingUpdateView, AppParkingDeleteView


urlpatterns = [
    url(r"^create/$", login_required(AppParkingCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppParkingUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppParkingDeleteView.as_view()), name="delete"),
]
