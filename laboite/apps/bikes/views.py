import json

from dal import autocomplete
from django import http

from boites.views import AppCreateView, AppUpdateView, AppDeleteView
from .forms import BikeModelForm
from .models import AppBikes
from .providers import get_provider


class StationAutoComplete(autocomplete.Select2ListView):
    def get_list(self):
        provider = get_provider(self.forwarded['provider'])
        if provider is not None:
            return provider.get_stations(self.q)
        return ()

    def get(self, request, *args, **kwargs):
        results = [{'id': id_, 'text': label} for id_, label in self.get_list()]
        return http.HttpResponse(json.dumps({'results': results}))


class AppBikesCreateView(AppCreateView):
    model = AppBikes
    form_class = BikeModelForm


class AppBikesUpdateView(AppUpdateView):
    model = AppBikes
    form_class = BikeModelForm


class AppBikesDeleteView(AppDeleteView):
    model = AppBikes
