from django.conf.urls import url

from .views import StationAutoComplete


urlpatterns = [
    url(
        r'^station-autocomplete/$',
        StationAutoComplete.as_view(),
        name='station-autocomplete',
    ),
]
