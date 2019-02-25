from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AppLuftdatenCreateView, AppLuftdatenUpdateView, AppLuftdatenDeleteView


urlpatterns = [
    url(r"^create/$", login_required(AppLuftdatenCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppLuftdatenUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppLuftdatenDeleteView.as_view()), name="delete"),
]
