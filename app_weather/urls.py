from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from .views import AppWeatherUpdateView

urlpatterns = [
    url(r"^(?P<pk>\d+)/$", login_required(AppWeatherUpdateView.as_view()), name="update"),
]
