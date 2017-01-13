from boites.views import AppCreateView, AppUpdateView, AppDeleteView
from .models import AppCalendar


class AppCalendarCreateView(AppCreateView):
    model = AppCalendar
    fields = ['ics_url']


class AppCalendarUpdateView(AppUpdateView):
    model = AppCalendar
    fields = ['ics_url',  'enabled']


class AppCalendarDeleteView(AppDeleteView):
    model = AppCalendar
