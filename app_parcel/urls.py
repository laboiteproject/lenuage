from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from .views import AppParcelUpdateView

urlpatterns = [
    url(r"^(?P<pk>\d+)/$", login_required(AppParcelUpdateView.as_view()), name="update"),
]
