from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from .views import AppCalendarUpdateView

urlpatterns = [
    url(r"^(?P<pk>\d+)/$", login_required(AppCalendarUpdateView.as_view()), name="update"),
]
