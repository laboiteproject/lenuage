import json

from dal import autocomplete
from django import http
from django.views.generic.edit import UpdateView

from .providers import get_provider
from .models import AppBikes


class StationAutoComplete(autocomplete.Select2ListView):
    def get_list(self):
        provider = get_provider(self.forwarded['provider'])
        if provider is not None:
            return provider.get_stations(self.q)
        return ()

    def get(self, request, *args, **kwargs):
        results = [{'id': id_, 'text': label} for id_, label in self.get_list()]
        return http.HttpResponse(json.dumps({'results': results}))

class AppBikesUpdateView(UpdateView):
    model = AppBikes
    fields = ['id_station']

    success_url = '../../'

    def get_context_data(self, **kwargs):
        context = super(AppBikesUpdateView, self).get_context_data(**kwargs)
        verbose_name = self.object._meta.verbose_name.title()
        context['verbose_name'] = verbose_name
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context
