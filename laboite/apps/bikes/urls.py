from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import StationAutoComplete, AppBikesCreateView, AppBikesUpdateView, AppBikesDeleteView


urlpatterns = [
    url(r'^station-autocomplete/$',
        login_required(StationAutoComplete.as_view()),
        name='station-autocomplete'),
    url(r"^create/$", login_required(AppBikesCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppBikesUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppBikesDeleteView.as_view()), name="delete"),
]
