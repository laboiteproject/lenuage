# coding: utf-8
from .models import AppCoffees
from boites.views import AppCreateView, AppUpdateView, AppDeleteView


class AppCoffeesCreateView(AppCreateView):
    model = AppCoffees
    fields = ['url', 'uid']


class AppCoffeesUpdateView(AppUpdateView):
    model = AppCoffees
    fields = ['url', 'uid', 'enabled']


class AppCoffeesDeleteView(AppDeleteView):
    model = AppCoffees
