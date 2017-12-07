# coding: utf-8
from __future__ import unicode_literals
from .models import AppCryptocurrency
from boites.views import AppCreateView, AppUpdateView, AppDeleteView


class AppCryptocurrencyCreateView(AppCreateView):
    model = AppCryptocurrency
    fields = ['cryptocurrency', 'currency']


class AppCryptocurrencyUpdateView(AppUpdateView):
    model = AppCryptocurrency
    fields = ['cryptocurrency', 'currency', 'enabled']


class AppCryptocurrencyDeleteView(AppDeleteView):
    model = AppCryptocurrency
