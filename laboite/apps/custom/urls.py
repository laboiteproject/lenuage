from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AppCustomCreateView, AppCustomUpdateView, AppCustomDeleteView


urlpatterns = [
    url(r"^create/$", login_required(AppCustomCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppCustomUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppCustomDeleteView.as_view()), name="delete"),
]
