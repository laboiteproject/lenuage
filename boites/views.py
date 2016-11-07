from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.contrib import messages

from .models import Boite

import json
import uuid
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

class BoiteListView(ListView):
    model = Boite

    def get_queryset(self):
        return Boite.objects.filter(user=self.request.user).order_by("created_date")

def json_view(request, api_key):
    boite = get_object_or_404(Boite, api_key=api_key)
    boite.last_connection = request.META.get("REMOTE_ADDR", "")
    boite.save()

    return JsonResponse(boite.get_apps_dictionary(), safe=False)

def generate_api_key(request, pk):
    boite = get_object_or_404(Boite, pk=pk, user=request.user)
    boite.api_key = uuid.uuid4()
    boite.save()

    return redirect('boites:update', pk=pk)

def get_prettyjson_html(api_key):
    boite = get_object_or_404(Boite, api_key=api_key)

    # Example from https://www.pydanny.com/pretty-formatting-json-django-admin.html
    response = json.dumps(boite.get_apps_dictionary(), sort_keys=True, indent=2)

    # Truncate the data. Alter as needed
    response = response[:5000]

    # Get the Pygments formatter
    formatter = HtmlFormatter(style='friendly')

    # Highlight the data
    response = highlight(response, JsonLexer(), formatter)

    # Get the stylesheet
    style = "<style>" + formatter.get_style_defs() + "</style><br>"

    # Safe the output
    return mark_safe(style + response)

class BoiteUpdateView(UpdateView):
    model = Boite
    fields = ['name']

    success_url = reverse_lazy('boites:list')

    def get_context_data(self, **kwargs):
        context = super(BoiteUpdateView, self).get_context_data(**kwargs)
        context['boite'] = self.object
        context['api_key'] = Boite._meta.get_field('api_key')
        context['last_activity'] = Boite._meta.get_field('last_activity')
        context['last_connection'] = Boite._meta.get_field('last_connection')
        context['pretty_json_html'] = get_prettyjson_html(self.object.api_key)

        return context

class BoiteDeleteView(DeleteView):
    model = Boite

    success_url = reverse_lazy('boites:list')

class BoiteCreateView(CreateView):
    model = Boite
    fields = ['name']
    template_name_suffix = '_create_form'
    success_message = "%(name)s was created successfully"

    success_url = reverse_lazy('boites:list')

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user

        return super(BoiteCreateView, self).form_valid(form)
