# coding: utf-8

from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.http import JsonResponse

from .models import AppEnergy
from boites.models import Boite

class AppEnergyUpdateView(SuccessMessageMixin, UpdateView):
    model = AppEnergy
    fields = ['url', 'power_feedid', 'kwhd_feedid', 'emoncms_read_apikey']

    success_message = _(u"App modifiée avec succès !")

    def get_context_data(self, **kwargs):
        context = super(AppEnergyUpdateView, self).get_context_data(**kwargs)
        verbose_name = self.object._meta.verbose_name.title()
        context['verbose_name'] = verbose_name
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context

    def get_success_url(self):
        return reverse_lazy('boites:update', kwargs={'pk': self.kwargs.get('boite_pk')})

class AppEnergyCreateView(SuccessMessageMixin, CreateView):
    model = AppEnergy
    fields = ['url', 'power_feedid', 'kwhd_feedid', 'emoncms_read_apikey', 'enabled']

    success_message = _(u"App a bien été créée !")

    def get_context_data(self, **kwargs):
        context = super(AppEnergyCreateView, self).get_context_data(**kwargs)
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context

    def get_success_url(self):
        return reverse_lazy('boites:update', kwargs={'pk': self.kwargs.get('boite_pk')})

    def form_valid(self, form):
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        form.instance.boite = boite
        form.save()
        return super(AppEnergyCreateView, self).form_valid(form)

class AppEnergyDeleteView(DeleteView):
    model = AppEnergy

    def get_context_data(self, **kwargs):
        context = super(AppEnergyDeleteView, self).get_context_data(**kwargs)
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context

    def get_success_url(self):
        messages.error(self.request, _(u"App supprimée !"))
        return reverse_lazy('boites:update', kwargs={'pk': self.kwargs.get('boite_pk')})
