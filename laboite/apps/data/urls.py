from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AppDataCreateView, AppDataUpdateView, AppDataDeleteView


urlpatterns = [
    url(r"^create/$", login_required(AppDataCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppDataUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppDataDeleteView.as_view()), name="delete"),
]
