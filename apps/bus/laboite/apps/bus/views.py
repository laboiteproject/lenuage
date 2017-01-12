# coding: utf-8

from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.http import HttpResponse

from dal.autocomplete import Select2ListView

from .models import AppBus
from .forms import AppBusForm
from boites.models import Boite

import requests
import json

from . import settings


class AppBusUpdateView(UpdateView):
    model = AppBus
    form_class = AppBusForm

    def get_context_data(self, **kwargs):
        context = super(AppBusUpdateView, self).get_context_data(**kwargs)
        verbose_name = self.object._meta.verbose_name.title()
        context['verbose_name'] = verbose_name
        context['boite_id'] = self.kwargs.get('boite_pk')
        return context

    def get_success_url(self):
        return reverse_lazy('boites:update', kwargs={'pk': self.kwargs.get('boite_pk')})


class AppBusCreateView(SuccessMessageMixin, CreateView):
    model = AppBus
    fields = ['stop']
    success_message = _(u"App a bien été créée !")

    def get_context_data(self, **kwargs):
        context = super(AppBusCreateView, self).get_context_data(**kwargs)
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context

    def get_success_url(self):
        return reverse_lazy('boites:update', kwargs={'pk': self.kwargs.get('boite_pk')})

    def form_valid(self, form):
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        form.instance.boite = boite
        form.save()
        return super(AppBusCreateView, self).form_valid(form)

class AppBusDeleteView(DeleteView):
    model = AppBus

    def get_context_data(self, **kwargs):
        context = super(AppBusDeleteView, self).get_context_data(**kwargs)
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context

    def get_success_url(self):
        messages.error(self.request, _(u"App supprimée !"))
        return reverse_lazy('boites:update', kwargs={'pk': self.kwargs.get('boite_pk')})

class BusStopAutocomplete(Select2ListView):
    def get(self, request, *args, **kwargs):
        directions = []

        if self.q:
            url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-circulation-passages-tr&rows=128&apikey="
            url += settings.STAR_API_KEY
            url += "&q="
            url += self.q

            r = requests.get(url)

            records = list(r.json()['records'])
            for record in records:
                destination = _(u"Arrêt") + " " + record['fields']['nomarret'] + " (" + record['fields']['nomcourtligne'] + " direction " + record['fields']['destination'] + ")"
                direction = {'id' :record['fields']['idarret'], 'text':destination}
                directions.append(direction)

        return HttpResponse(json.dumps({"results" : directions}))
