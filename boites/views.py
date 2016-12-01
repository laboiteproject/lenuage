# coding: utf-8

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.apps import apps

from .models import Boite, App

import json
import uuid
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

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

        apps_list = []
        for model in apps.get_models():
            if issubclass(model, App):
                app_instances = model.objects.filter(boite=self.object)
                pk = None
                if app_instances:
                    first_app = app_instances.first()
                    pk = first_app.pk

                verbose_name =  model._meta.verbose_name.title()
                apps_list.append({'verbose_name':verbose_name[16:], 'pk':pk, 'app_label': model._meta.app_label})

        context['apps'] = apps_list

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
