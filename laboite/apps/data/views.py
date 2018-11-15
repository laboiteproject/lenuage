# coding: utf-8
from __future__ import unicode_literals
from django.utils.safestring import mark_safe
from .models import AppData
from boites.views import AppCreateView, AppUpdateView, AppDeleteView

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

class AppDataCreateView(AppCreateView):
    model = AppData
    fields = ['url', 'prepend', 'append']

class AppDataUpdateView(AppUpdateView):
    model = AppData
    fields = ['url', 'prepend', 'append', 'json_path', 'enabled']

class AppDataDeleteView(AppDeleteView):
    model = AppData
