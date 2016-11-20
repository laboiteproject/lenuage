from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib import admin
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
    url(r"^(?P<boite_pk>\d+)/app_bus/", include('app_bus.urls', namespace="app_bus")),
    url(r"^(?P<boite_pk>\d+)/app_bikes/", include('app_bikes.urls', namespace="app_bikes")),
    url(r"^(?P<boite_pk>\d+)/app_time/", include('app_time.urls', namespace="app_time")),
    url(r"^(?P<boite_pk>\d+)/app_weather/", include('app_weather.urls', namespace="app_weather")),
    url(r"^(?P<boite_pk>\d+)/app_traffic/", include('app_traffic.urls', namespace="app_traffic")),
    url(r"^(?P<boite_pk>\d+)/app_tasks/", include('app_tasks.urls', namespace="app_tasks")),
    url(r"^(?P<boite_pk>\d+)/app_calendar/", include('app_calendar.urls', namespace="app_calendar")),
    url(r"^(?P<boite_pk>\d+)/app_parcel/", include('app_parcel.urls', namespace="app_parcel")),
    url(r"^(?P<boite_pk>\d+)/app_messages/", include('app_messages.urls', namespace="app_messages")),
    url(r'^(?P<api_key>[0-9a-z-]+)/$', json_view, name='json'),
    url(r'^redirect/(?P<api_key>[0-9a-z-]+)/$', login_required(redirect_view), name="redirect"),
]

#
# for model in apps.get_models():
#     if issubclass(model, App):
#         app_label = model._meta.app_label
#         url(r"^(?P<boite_pk>\d+)/" + app_label, include(app_label + '.urls', namespace=app_label))

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
