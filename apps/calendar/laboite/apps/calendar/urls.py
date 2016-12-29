from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from .views import AppCalendarUpdateView, AppCalendarCreateView, AppCalendarDeleteView

urlpatterns = [
    url(r"^create/$", login_required(AppCalendarCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppCalendarUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppCalendarDeleteView.as_view()), name="delete"),
]
