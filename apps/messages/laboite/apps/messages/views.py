# coding: utf-8

from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from .models import AppMessages
from boites.models import Boite

class AppMessagesUpdateView(SuccessMessageMixin, UpdateView):
    model = AppMessages
    fields = ['message', 'enabled']
    success_message = _(u"App modifiée avec succès !")

    def get_context_data(self, **kwargs):
        context = super(AppMessagesUpdateView, self).get_context_data(**kwargs)
        verbose_name = self.object._meta.verbose_name.title()
        context['verbose_name'] = verbose_name
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context

    def get_success_url(self):
        return reverse_lazy('boites:update', kwargs={'pk': self.kwargs.get('boite_pk')})

class AppMessagesCreateView(SuccessMessageMixin, CreateView):
    model = AppMessages
    fields = ['message']
    success_message = _(u"App a bien été créée !")

    def get_context_data(self, **kwargs):
        context = super(AppMessagesCreateView, self).get_context_data(**kwargs)
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context

    def get_success_url(self):
        return reverse_lazy('boites:update', kwargs={'pk': self.kwargs.get('boite_pk')})

    def form_valid(self, form):
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        form.instance.boite = boite
        form.save()
        return super(AppMessagesCreateView, self).form_valid(form)

class AppMessagesDeleteView(DeleteView):
    model = AppMessages

    def get_context_data(self, **kwargs):
        context = super(AppMessagesDeleteView, self).get_context_data(**kwargs)
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context

    def get_success_url(self):
        messages.error(self.request, _(u"App supprimée !"))
        return reverse_lazy('boites:update', kwargs={'pk': self.kwargs.get('boite_pk')})
