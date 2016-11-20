from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import StationAutoComplete, AppBikesUpdateView


urlpatterns = [
    url(
        r'^station-autocomplete/$',
        StationAutoComplete.as_view(),
        name='station-autocomplete',
    ),
    url(r"^(?P<pk>\d+)/$", login_required(AppBikesUpdateView.as_view()), name="update"),
]
