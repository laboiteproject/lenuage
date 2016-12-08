from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from .views import AppTimeUpdateView, AppTimeCreateView, AppTimeDeleteView

urlpatterns = [
    url(r"^create/$", login_required(AppTimeCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppTimeUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppTimeDeleteView.as_view()), name="delete"),
]
