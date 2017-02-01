# coding: utf-8

from django.http import JsonResponse

from .models import AppTasks, get_projects
from boites.views import AppCreateView, AppUpdateView, AppDeleteView
from .forms import TasksModelForm


def get_projects_view(request, *args, **kw):
    access_token = request.GET.get('access_token')
    projects = get_projects(access_token)
    return JsonResponse(projects, safe=False)


class AppTasksCreateView(AppCreateView):
    model = AppTasks
    form_class = TasksModelForm


class AppTasksUpdateView(AppUpdateView):
    model = AppTasks
    form_class = TasksModelForm


class AppTasksDeleteView(AppDeleteView):
    model = AppTasks
