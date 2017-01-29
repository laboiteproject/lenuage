from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AppTrafficCreateView, AppTrafficUpdateView, AppTrafficDeleteView


urlpatterns = [
    url(r"^create/$", login_required(AppTrafficCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppTrafficUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppTrafficDeleteView.as_view()), name="delete"),
]
