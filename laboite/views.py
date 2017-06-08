from django.shortcuts import render
from django.apps import apps

from boites.models import Boite, App

def home_view(request):
    apps_list = []
    for model in apps.get_models():
        if issubclass(model, App):
            verbose_name =  model._meta.verbose_name.title()
            apps_list.append({'verbose_name':verbose_name[16:], 'pk':'create', 'app_label': model._meta.app_label})

    return render(request, 'homepage.html', {'apps': apps_list})
