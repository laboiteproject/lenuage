from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AppParcelUpdateView, AppParcelCreateView, AppParcelDeleteView


urlpatterns = [
    url(r"^create/$", login_required(AppParcelCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppParcelUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppParcelDeleteView.as_view()), name="delete"),
]
