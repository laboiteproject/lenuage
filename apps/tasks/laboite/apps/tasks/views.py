# coding: utf-8

from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.http import JsonResponse

from .models import AppTasks
from boites.models import Boite

import asana


def get_projects_view(request, pk, boite_pk):
    app_tasks = get_object_or_404(AppTasks, pk=pk)
    projects = get_projects(app_tasks.asana_personal_access_token)

    return JsonResponse(projects, safe=False)

def get_projects(asana_personal_access_token):
    client = asana.Client.access_token(asana_personal_access_token)
    workspaces = client.workspaces.find_all()
    results = []
    for workspace in workspaces:
        projects = client.projects.find_all({'workspace': workspace['id']})
        for project in projects:
            results.append({'id': project['id'],'name': project['name']})
    return results

class AppTasksUpdateView(SuccessMessageMixin, UpdateView):
    model = AppTasks
    fields = ['asana_personal_access_token', 'asana_project_id', 'enabled']

    success_message = _(u"App modifiée avec succès !")

    def get_context_data(self, **kwargs):
        context = super(AppTasksUpdateView, self).get_context_data(**kwargs)
        verbose_name = self.object._meta.verbose_name.title()
        context['verbose_name'] = verbose_name
        context['boite_id'] = self.kwargs.get('boite_pk')
        context['asana_personal_access_token'] = self.object.asana_personal_access_token

        return context

    def get_success_url(self):
        return reverse_lazy('boites:update', kwargs={'pk': self.kwargs.get('boite_pk')})

class AppTasksCreateView(SuccessMessageMixin, CreateView):
    model = AppTasks
    fields = ['asana_personal_access_token']
    template_name = 'apptasks_create_form.html'

    success_message = _(u"App a bien été créée !")

    def get_context_data(self, **kwargs):
        context = super(AppTasksCreateView, self).get_context_data(**kwargs)
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context

    def get_success_url(self):
        return reverse_lazy('boites:update', kwargs={'pk': self.kwargs.get('boite_pk')})

    def form_valid(self, form):
        boite = get_object_or_404(Boite, pk=self.kwargs.get('boite_pk'), user=self.request.user)
        form.instance.boite = boite
        form.save()
        return super(AppTasksCreateView, self).form_valid(form)

class AppTasksDeleteView(DeleteView):
    model = AppTasks

    def get_context_data(self, **kwargs):
        context = super(AppTasksDeleteView, self).get_context_data(**kwargs)
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context

    def get_success_url(self):
        messages.error(self.request, _(u"App supprimée !"))
        return reverse_lazy('boites:update', kwargs={'pk': self.kwargs.get('boite_pk')})
