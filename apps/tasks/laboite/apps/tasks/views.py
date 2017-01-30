# coding: utf-8

from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import AppTasks
from boites.views import AppCreateView, AppUpdateView, AppDeleteView

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
            results.append({'id': project['id'],
                            'name': project['name']})
    return results


class AppTasksCreateView(AppCreateView):
    model = AppTasks
    fields = ['asana_personal_access_token', 'asana_project_id', 'enabled']
    template_name = 'laboite.apps.tasks/apptasks_form.html'

    class Media:
        js = ('js/form.js',)

    def get_context_data(self, **kwargs):
        context = super(AppTasksCreateView, self).get_context_data(**kwargs)
        context['asana_personal_access_token'] = ''
        return context


class AppTasksUpdateView(AppUpdateView):
    model = AppTasks
    fields = ['asana_personal_access_token', 'asana_project_id', 'enabled']
    template_name = 'laboite.apps.tasks/apptasks_form.html'

    class Media:
        js = ('js/form.js',)

    def get_context_data(self, **kwargs):
        context = super(AppTasksUpdateView, self).get_context_data(**kwargs)
        context['asana_personal_access_token'] = self.object.asana_personal_access_token
        context['projects'] = get_projects(self.object.asana_personal_access_token)
        return context


class AppTasksDeleteView(AppDeleteView):
    model = AppTasks
