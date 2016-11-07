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
)

urlpatterns = [
    url(r"^$", login_required(BoiteListView.as_view()), name="list"),
    url(r"^create/$", login_required(BoiteCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/settings/$", login_required(BoiteUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(BoiteDeleteView.as_view()), name="delete"),
    url(r"^(?P<pk>\d+)/generate/$", login_required(generate_api_key), name="generate"),
    url(r'^(?P<api_key>[0-9a-z-]+)/$', json_view, name='json'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
