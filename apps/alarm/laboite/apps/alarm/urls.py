from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AppAlarmCreateView, AppAlarmUpdateView, AppAlarmDeleteView


urlpatterns = [
    url(r"^create/$", login_required(AppAlarmCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppAlarmUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppAlarmDeleteView.as_view()), name="delete"),
]
