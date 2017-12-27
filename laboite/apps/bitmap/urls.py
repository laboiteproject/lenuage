from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AppBitmapCreateView, AppBitmapUpdateView, AppBitmapDeleteView


urlpatterns = [
    url(r"^create/$", login_required(AppBitmapCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppBitmapUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppBitmapDeleteView.as_view()), name="delete"),
]
