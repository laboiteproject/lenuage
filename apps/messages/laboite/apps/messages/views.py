# coding: utf-8

from .models import AppMessages
from boites.views import AppCreateView, AppUpdateView, AppDeleteView


class AppMessagesCreateView(AppCreateView):
    model = AppMessages
    fields = ['message']


class AppMessagesUpdateView(AppUpdateView):
    model = AppMessages
    fields = ['message', 'enabled']


class AppMessagesDeleteView(AppDeleteView):
    model = AppMessages
