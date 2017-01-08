from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib.auth.decorators import login_required

from .views import (
    BoiteListView,
    BoiteCreateView,
    BoiteUpdateView,
    BoiteDeleteView,
    json_view,
    generate_api_key,
    redirect_view,
)

urlpatterns = [
    url(r"^$", login_required(BoiteListView.as_view()), name="list"),
    url(r"^create/$", login_required(BoiteCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(BoiteUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(BoiteDeleteView.as_view()), name="delete"),
    url(r"^(?P<pk>\d+)/generate/$", login_required(generate_api_key), name="generate"),
    url(r"^(?P<boite_pk>\d+)/apps/bus/", include('laboite.apps.bus.urls', namespace="apps_bus")),
    url(r"^(?P<boite_pk>\d+)/apps/bikes/", include('laboite.apps.bikes.urls', namespace="app_bikes")),
    url(r"^(?P<boite_pk>\d+)/apps/time/", include('laboite.apps.time.urls', namespace="app_time")),
    url(r"^(?P<boite_pk>\d+)/apps/weather/", include('laboite.apps.weather.urls', namespace="app_weather")),
    url(r"^(?P<boite_pk>\d+)/apps/traffic/", include('laboite.apps.traffic.urls', namespace="app_traffic")),
    url(r"^(?P<boite_pk>\d+)/apps/tasks/", include('laboite.apps.tasks.urls', namespace="app_tasks")),
    url(r"^(?P<boite_pk>\d+)/apps/calendar/", include('laboite.apps.calendar.urls', namespace="app_calendar")),
    url(r"^(?P<boite_pk>\d+)/apps/parcel/", include('laboite.apps.parcel.urls', namespace="app_parcel")),
    url(r"^(?P<boite_pk>\d+)/apps/messages/", include('laboite.apps.messages.urls', namespace="app_messages")),
    url(r"^(?P<boite_pk>\d+)/apps/metro/", include('laboite.apps.metro.urls', namespace="app_metro")),
    url(r'^(?P<api_key>[0-9a-z-]+)/$', json_view, name='json'),
    url(r'^redirect/(?P<api_key>[0-9a-z-]+)/$', login_required(redirect_view), name="redirect"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
