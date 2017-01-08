from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from .views import AppWeatherUpdateView, AppWeatherCreateView, AppWeatherDeleteView

urlpatterns = [
    url(r"^create/$", login_required(AppWeatherCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppWeatherUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppWeatherDeleteView.as_view()), name="delete"),
]
