# coding: utf-8
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppCoffeesConfig(AppConfig):
    name = label = 'laboite.apps.coffees'
    verbose_name = _('App : Cafés')
