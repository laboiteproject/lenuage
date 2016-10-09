from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib import admin

from .views import BoiteDetailView, json_view


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', BoiteDetailView.as_view(), name='boite-detail'),
    url(r'^(?P<pk>[0-9]+)/json/$', json_view, name='boite-json'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
