# coding: utf-8

from __future__ import unicode_literals
import json

from django.apps import apps
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

from .models import App, Boite


# Boîtes

class BoiteListView(ListView):
    model = Boite

    def get_queryset(self):
        boites = Boite.objects.filter(qrcode=None)
        for boite in boites:
            boite.generate_qrcode()
            boite.save()

        return Boite.objects.filter(user=self.request.user).order_by("created_date")


def json_view(request, api_key):
    boite = get_object_or_404(Boite, api_key=api_key)
    boite.last_connection = request.META.get("REMOTE_ADDR", "")
    boite.save()
    return JsonResponse(boite.get_apps_dictionary(), safe=False)

def create_app_view(request, pk):
    boite = get_object_or_404(Boite, pk=pk, user=request.user)

    apps_list = []
    for model in apps.get_models():
        if issubclass(model, App):
            app_instances = model.objects.filter(boite=boite)
            verbose_name =  model._meta.verbose_name.title()
            if not app_instances:
                apps_list.append({'verbose_name':verbose_name[16:], 'pk':'create', 'app_label': model._meta.app_label})

    return render(request, 'boites/boite_create_app.html', {'boite': boite, 'boite_id': boite.id, 'apps': apps_list})


def apps_view(request, pk):
    boite = get_object_or_404(Boite, pk=pk, user=request.user)

    apps_list = []
    enabled_apps = 0
    for model in apps.get_models():
        if issubclass(model, App):
            app_instances = model.objects.filter(boite=boite)
            pk = None
            enabled = None

            if app_instances:
                first_app = app_instances.first()
                pk = first_app.pk
                enabled = first_app.enabled
                enabled_apps += 1

            verbose_name =  model._meta.verbose_name.title()
            apps_list.append({'verbose_name':verbose_name[16:], 'pk':pk, 'enabled':enabled, 'app_label': model._meta.app_label})

    return render(request, 'boites/boite_apps.html', {'boite': boite, 'boite_id': boite.id, 'apps': apps_list, 'show_create_button' : len(apps_list) > enabled_apps})


def redirect_view(request, api_key):
    boite = get_object_or_404(Boite, api_key=api_key)
    return redirect('boites:update', pk=boite.pk)


def generate_api_key(request, pk):
    boite = get_object_or_404(Boite, pk=pk, user=request.user)
    boite.generate_api_key()
    boite.save()
    return redirect('boites:update', pk=pk)


def get_prettyjson_html(api_key):
    boite = get_object_or_404(Boite, api_key=api_key)
    # Example from https://www.pydanny.com/pretty-formatting-json-django-admin.html
    response = json.dumps(boite.get_apps_dictionary(), sort_keys=True, indent=2)
    response = response[:5000]
    formatter = HtmlFormatter(style='friendly')
    response = highlight(response, JsonLexer(), formatter)
    style = "<style>" + formatter.get_style_defs() + "</style><br>"
    return mark_safe(style + response)


class BoiteUpdateView(UpdateView):
    model = Boite
    fields = ['name']

    success_url = reverse_lazy('boites:list')

    def get_context_data(self, **kwargs):
        context = super(BoiteUpdateView, self).get_context_data(**kwargs)
        context['boite'] = self.object
        context['boite_id'] = self.object.id
        context['api_key'] = Boite._meta.get_field('api_key')
        context['last_activity'] = Boite._meta.get_field('last_activity')
        context['last_connection'] = Boite._meta.get_field('last_connection')
        context['pretty_json_html'] = get_prettyjson_html(self.object.api_key)

        return context


class BoiteDeleteView(DeleteView):
    model = Boite
    success_url = reverse_lazy('boites:list')

    def get_context_data(self, **kwargs):
        context = super(BoiteDeleteView, self).get_context_data(**kwargs)
        context['boite_id'] = self.object.id
        return context


class BoiteCreateView(SuccessMessageMixin, CreateView):
    model = Boite
    fields = ['name']
    template_name_suffix = '_create_form'
    success_message = _(u"%(name)s a bien été créé !")
    success_url = reverse_lazy('boites:list')

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(BoiteCreateView, self).form_valid(form)


# Apps

class AppCreateView(SuccessMessageMixin, CreateView):
    template_name = 'apps/app_form.html'
    success_message = _('App a bien été créée !')

    def get_context_data(self, **kwargs):
        context = super(AppCreateView, self).get_context_data(**kwargs)
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        context['boite'] = boite
        context['boite_id'] = self.kwargs.get('boite_pk')
        return context

    def get_success_url(self):
        return reverse_lazy('boites:apps', kwargs={'pk': self.kwargs.get('boite_pk')})

    def form_valid(self, form):
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        form.instance.boite = boite
        form.save()
        return super(AppCreateView, self).form_valid(form)


class AppUpdateView(UpdateView):
    template_name = 'apps/app_form.html'

    def get_context_data(self, **kwargs):
        context = super(AppUpdateView, self).get_context_data(**kwargs)
        verbose_name = self.object._meta.verbose_name.title()
        context['verbose_name'] = verbose_name[16:]
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        context['boite'] = boite
        context['boite_id'] = self.kwargs.get('boite_pk')
        return context

    def get_success_url(self):
        return reverse_lazy('boites:apps', kwargs={'pk': self.kwargs.get('boite_pk')})


class AppDeleteView(DeleteView):
    template_name = 'apps/app_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(AppDeleteView, self).get_context_data(**kwargs)
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        context['boite'] = boite
        context['boite_id'] = self.kwargs.get('boite_pk')
        return context

    def get_success_url(self):
        messages.error(self.request, _('App supprimée !'))
        return reverse_lazy('boites:apps', kwargs={'pk': self.kwargs.get('boite_pk')})
