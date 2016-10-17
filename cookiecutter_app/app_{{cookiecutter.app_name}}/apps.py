from __future__ import unicode_literals

from django.apps import AppConfig

class App{{cookiecutter.app_model_name}}Config(AppConfig):
    name = 'app_{{cookiecutter.app_name}}'
    verbose_name = 'App : {{cookiecutter.app_verbose_name}}'
