from django.conf import settings
from django.urls import include, path
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
    path("", login_required(BoiteListView.as_view()), name="list"),
    path("create$", login_required(BoiteCreateView.as_view()), name="create"),
    path("<int:pk>$", login_required(BoiteUpdateView.as_view()), name="update"),
    path("<int:pk>/delete$", login_required(BoiteDeleteView.as_view()), name="delete"),
    path("<int:pk>/generate$", login_required(generate_api_key), name="generate"),
    path("<int:pk>/apps$", login_required(apps_view), name="apps"),
    path("<int:pk>/apps/create$", login_required(create_app_view), name="create_app"),
    path("<int:pk>/pushbutton$", login_required(PushButtonUpdateView.as_view()), name="pushbutton"),
    path('<slug:api_key>/pushbutton/', trigger_pushbutton_json_view, name='trigger_pushbutton'),
    path("<int:boite_pk>/tiles/<int:pk>$", TileUpdateView.as_view(), name="tile"),
    path("<slug:api_key>/tiles/<int:pk>$", tile_json_view, name="tile_json"),
    path("<int:boite_pk>/tiles/<int:pk>/create$", login_required(create_tile_view), name="create_tile"),
    path("<int:boite_pk>/tiles/<int:pk>/delete$", login_required(TileDeleteView.as_view()), name="delete_tile"),
    path("<int:boite_pk>/tiles/<int:pk>/app$", login_required(tileapp_view), name="tileapp"),
    path("<int:boite_pk>/tiles/<int:tile_pk>/app/<int:pk>/delete$", login_required(TileAppDeleteView.as_view()), name="delete_tileapp"),
    path("<int:boite_pk>/tiles/editor", login_required(tile_editor_view), name="editor"),
    # Apps
    path("<int:boite_pk>/apps/bus/", include('laboite.apps.bus.urls', namespace="apps_bus")),
    path("<int:boite_pk>/apps/bikes/", include('laboite.apps.bikes.urls', namespace="app_bikes")),
    path("<int:boite_pk>/apps/calendar/", include('laboite.apps.calendar.urls', namespace="app_calendar")),
    path("<int:boite_pk>/apps/energy/", include('laboite.apps.energy.urls', namespace="app_energy")),
    path("<int:boite_pk>/apps/messages/", include('laboite.apps.messages.urls', namespace="app_messages")),
    path("<int:boite_pk>/apps/metro/", include('laboite.apps.metro.urls', namespace="app_metro")),
    path("<int:boite_pk>/apps/parcel/", include('laboite.apps.parcel.urls', namespace="app_parcel")),
    path("<int:boite_pk>/apps/tasks/", include('laboite.apps.tasks.urls', namespace="app_tasks")),
    path("<int:boite_pk>/apps/time/", include('laboite.apps.time.urls', namespace="app_time")),
    path("<int:boite_pk>/apps/traffic/", include('laboite.apps.traffic.urls', namespace="app_traffic")),
    path("<int:boite_pk>/apps/weather/", include('laboite.apps.weather.urls', namespace="app_weather")),
    path("<int:boite_pk>/apps/wifi/", include('laboite.apps.wifi.urls', namespace="app_wifi")),
    path("<int:boite_pk>/apps/likes/", include('laboite.apps.likes.urls', namespace="app_likes")),
    path("<int:boite_pk>/apps/bitmap/", include('laboite.apps.bitmap.urls', namespace="app_bitmap")),
    path("<int:boite_pk>/apps/parking/", include('laboite.apps.parking.urls', namespace="app_parking")),
    path("<int:boite_pk>/apps/coffees/", include('laboite.apps.coffees.urls', namespace="app_coffees")),
    path("<int:boite_pk>/apps/cryptocurrency/", include('laboite.apps.cryptocurrency.urls', namespace="app_cryptocurrency")),
    path("<int:boite_pk>/apps/data/", include('laboite.apps.data.urls', namespace="app_data")),
    path("<int:boite_pk>/apps/airquality/", include('laboite.apps.airquality.urls', namespace="app_airquality")),
    path("<int:boite_pk>/apps/luftdaten/", include('laboite.apps.luftdaten.urls', namespace="app_luftdaten")),
    path('<slug:api_key>/', boite_json_view, name='json'),
    path('redirect/<slug:api_key>', login_required(redirect_view), name="redirect"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
