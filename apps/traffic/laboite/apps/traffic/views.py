from boites.views import AppCreateView, AppUpdateView, AppDeleteView
from .models import AppTraffic


class AppTrafficCreateView(AppCreateView):
    model = AppTraffic
    fields = ['mode', 'start', 'dest']


class AppTrafficUpdateView(AppUpdateView):
    model = AppTraffic
    fields = ['mode', 'start', 'dest', 'enabled']


class AppTrafficDeleteView(AppDeleteView):
    model = AppTraffic
