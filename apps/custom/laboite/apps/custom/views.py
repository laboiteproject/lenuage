# coding: utf-8
from __future__ import unicode_literals
from .models import AppCustom
from boites.views import AppCreateView, AppUpdateView, AppDeleteView


class AppCustomCreateView(AppCreateView):
    model = AppCustom
    template_name = 'custom_form.html'
    fields = ['some_field_name']


class AppCustomUpdateView(AppUpdateView):
    model = AppCustom
    template_name = 'custom_form.html'
    fields = ['some_field_name', 'enabled']


class AppCustomDeleteView(AppDeleteView):
    model = AppCustom
