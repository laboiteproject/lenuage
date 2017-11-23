# coding: utf-8
from __future__ import unicode_literals

import requests
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from boites.exceptions import ExternalDataError
from boites.models import App, MINUTES

MODES = (
    ('driving', 'En voiture'),
    ('walking', 'A pied'),
    ('bicycling', 'A vélo'),
    ('transit', 'En transport en commun')
)


class AppTraffic(App):
    UPDATE_INTERVAL = 15 * MINUTES

    mode = models.CharField(_('Mode de transport'), choices=MODES, max_length=32, null=True, default='driving')
    start = models.CharField(_('Point de départ'), max_length=1024,  null=True, default=None)
    dest = models.CharField(_('Destination'), max_length=1024, null=True, default=None)
    trajectory_name = models.CharField(_('Itinéraire'), max_length=128, null=True, default=None)
    trip_duration = models.PositiveSmallIntegerField(_('Durée'), null=True, default=None)

    def update_data(self):
        params = {'origin': self.start,
                  'destination': self.dest,
                  'mode': self.mode,
                  'key': settings.GOOGLE_MAPS_API_KEY}
        r = requests.get(settings.GOOGLE_MAPS_BASE_URL, params=params)
        routes = r.json().get('routes')
        all_routes = []
        for route in routes:
            duration = sum(leg['duration']['value'] for leg in route['legs']) / 60
            all_routes.append({'trajectory_name': route['summary'],
                               'trip_duration': duration})
        if all_routes:
            all_routes.sort(key=lambda route: route['trip_duration'])
            best_route = all_routes.pop(0)
            self.trajectory_name = best_route['trajectory_name']
            self.trip_duration = best_route['trip_duration']
            self.save()
        else:
            raise ExternalDataError('No route found')

    def _get_data(self):
        return {'start': self.start,
                'dest': self.dest,
                'trajectory_name': self.trajectory_name,
                'trip_duration': self.trip_duration}

    class Meta:
        verbose_name = _('Configuration : trafic')
        verbose_name_plural = _('Configurations : trafic')
