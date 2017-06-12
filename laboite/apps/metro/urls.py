from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AppMetroUpdateView, AppMetroCreateView, AppMetroDeleteView

urlpatterns = [
    url(r"^create/$", login_required(AppMetroCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppMetroUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppMetroDeleteView.as_view()), name="delete"),
]
