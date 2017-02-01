# coding: utf-8

from boites.views import AppCreateView, AppUpdateView, AppDeleteView
from .models import AppParcel


class AppParcelCreateView(AppCreateView):
    model = AppParcel
    fields = ['parcel', 'parcel_carrier']


class AppParcelUpdateView(AppUpdateView):
    model = AppParcel
    fields = ['parcel', 'parcel_carrier', 'enabled']


class AppParcelDeleteView(AppDeleteView):
    model = AppParcel
