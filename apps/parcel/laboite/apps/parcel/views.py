# coding: utf-8

from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from boites.models import Boite
from .models import AppParcel


class AppParcelUpdateView(UpdateView):
    model = AppParcel
    fields = ['parcel', 'parcel_carrier', 'enabled']

    def get_context_data(self, **kwargs):
        context = super(AppParcelUpdateView, self).get_context_data(**kwargs)
        verbose_name = self.object._meta.verbose_name.title()
        context['verbose_name'] = verbose_name
        context['boite_id'] = self.kwargs.get('boite_pk')
        return context

    def get_success_url(self):
        return reverse_lazy('boites:update', kwargs={'pk': self.kwargs.get('boite_pk')})


class AppParcelCreateView(SuccessMessageMixin, CreateView):
    model = AppParcel
    fields = ['parcel', 'parcel_carrier']
    success_message = _(u"App a bien été créée !")

    def get_context_data(self, **kwargs):
        context = super(AppParcelCreateView, self).get_context_data(**kwargs)
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context

    def get_success_url(self):
        return reverse_lazy('boites:update', kwargs={'pk': self.kwargs.get('boite_pk')})

    def form_valid(self, form):
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        form.instance.boite = boite
        form.save()
        return super(AppParcelCreateView, self).form_valid(form)

class AppParcelDeleteView(DeleteView):
    model = AppParcel

    def get_context_data(self, **kwargs):
        context = super(AppParcelDeleteView, self).get_context_data(**kwargs)
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context

    def get_success_url(self):
        messages.error(self.request, _(u"App supprimée !"))
        return reverse_lazy('boites:update', kwargs={'pk': self.kwargs.get('boite_pk')})
