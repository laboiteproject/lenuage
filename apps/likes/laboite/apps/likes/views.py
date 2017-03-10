# coding: utf-8
from __future__ import unicode_literals
from .models import AppLikes
from boites.views import AppCreateView, AppUpdateView, AppDeleteView


class AppLikesCreateView(AppCreateView):
    model = AppLikes
    fields = ['page_name']


class AppLikesUpdateView(AppUpdateView):
    model = AppLikes
    fields = ['page_name', 'enabled']


class AppLikesDeleteView(AppDeleteView):
    model = AppLikes
