from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib.auth.decorators import login_required

from .api import boite_json_view, tile_json_view, trigger_pushbutton_json_view
from .views import (
    BoiteListView,
    BoiteCreateView,
    BoiteUpdateView,
    BoiteDeleteView,
    generate_api_key,
    redirect_view,
    apps_view,
    create_app_view,
    tile_editor_view,
    TileUpdateView,
    TileDeleteView,
    tileapp_view,
    create_tile_view,
    TileAppDeleteView,
    PushButtonUpdateView,
)

urlpatterns = [
    url(r"^$", login_required(BoiteListView.as_view()), name="list"),
    url(r"^create/$", login_required(BoiteCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(BoiteUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(BoiteDeleteView.as_view()), name="delete"),
    url(r"^(?P<pk>\d+)/generate/$", login_required(generate_api_key), name="generate"),
    url(r"^(?P<pk>\d+)/apps/$", login_required(apps_view), name="apps"),
    url(r"^(?P<pk>\d+)/apps/create/$", login_required(create_app_view), name="create_app"),
    url(r"^(?P<pk>\d+)/pushbutton/$", login_required(PushButtonUpdateView.as_view()), name="pushbutton"),
    url(r'^(?P<api_key>[0-9a-z-]+)/pushbutton/$', trigger_pushbutton_json_view, name='trigger_pushbutton'),
    url(r"^(?P<boite_pk>\d+)/tiles/(?P<pk>\d+)/$", TileUpdateView.as_view(), name="tile"),
    url(r"^(?P<api_key>[0-9a-z-]+)/tiles/(?P<pk>\d+)/$", tile_json_view, name="tile_json"),
    url(r"^(?P<boite_pk>\d+)/tiles/(?P<pk>\d+)/create/$", login_required(create_tile_view), name="create_tile"),
    url(r"^(?P<boite_pk>\d+)/tiles/(?P<pk>\d+)/delete/$", login_required(TileDeleteView.as_view()), name="delete_tile"),
    url(r"^(?P<boite_pk>\d+)/tiles/(?P<pk>\d+)/app/$", login_required(tileapp_view), name="tileapp"),
    url(r"^(?P<boite_pk>\d+)/tiles/(?P<tile_pk>\d+)/app/(?P<pk>\d+)/delete/$", login_required(TileAppDeleteView.as_view()), name="delete_tileapp"),
    url(r"^(?P<boite_pk>\d+)/tiles/editor/$", login_required(tile_editor_view), name="editor"),
    # Apps
    url(r"^(?P<boite_pk>\d+)/apps/bus/", include('laboite.apps.bus.urls', namespace="apps_bus")),
    url(r"^(?P<boite_pk>\d+)/apps/bikes/", include('laboite.apps.bikes.urls', namespace="app_bikes")),
    url(r"^(?P<boite_pk>\d+)/apps/calendar/", include('laboite.apps.calendar.urls', namespace="app_calendar")),
    url(r"^(?P<boite_pk>\d+)/apps/energy/", include('laboite.apps.energy.urls', namespace="app_energy")),
    url(r"^(?P<boite_pk>\d+)/apps/messages/", include('laboite.apps.messages.urls', namespace="app_messages")),
    url(r"^(?P<boite_pk>\d+)/apps/metro/", include('laboite.apps.metro.urls', namespace="app_metro")),
    url(r"^(?P<boite_pk>\d+)/apps/parcel/", include('laboite.apps.parcel.urls', namespace="app_parcel")),
    url(r"^(?P<boite_pk>\d+)/apps/tasks/", include('laboite.apps.tasks.urls', namespace="app_tasks")),
    url(r"^(?P<boite_pk>\d+)/apps/time/", include('laboite.apps.time.urls', namespace="app_time")),
    url(r"^(?P<boite_pk>\d+)/apps/traffic/", include('laboite.apps.traffic.urls', namespace="app_traffic")),
    url(r"^(?P<boite_pk>\d+)/apps/weather/", include('laboite.apps.weather.urls', namespace="app_weather")),
    url(r"^(?P<boite_pk>\d+)/apps/wifi/", include('laboite.apps.wifi.urls', namespace="app_wifi")),
    url(r"^(?P<boite_pk>\d+)/apps/likes/", include('laboite.apps.likes.urls', namespace="app_likes")),
    url(r"^(?P<boite_pk>\d+)/apps/bitmap/", include('laboite.apps.bitmap.urls', namespace="app_bitmap")),
    url(r"^(?P<boite_pk>\d+)/apps/parking/", include('laboite.apps.parking.urls', namespace="app_parking")),
    url(r"^(?P<boite_pk>\d+)/apps/coffees/", include('laboite.apps.coffees.urls', namespace="app_coffees")),
    url(r"^(?P<boite_pk>\d+)/apps/cryptocurrency/", include('laboite.apps.cryptocurrency.urls', namespace="app_cryptocurrency")),
    url(r"^(?P<boite_pk>\d+)/apps/data/", include('laboite.apps.data.urls', namespace="app_data")),
    url(r'^(?P<api_key>[0-9a-z-]+)/$', boite_json_view, name='json'),
    url(r'^redirect/(?P<api_key>[0-9a-z-]+)/$', login_required(redirect_view), name="redirect"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
