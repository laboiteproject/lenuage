# coding: utf-8
from __future__ import unicode_literals

import requests
from django.utils.translation import ugettext_lazy as _
from django.db import models

from boites.exceptions import ExternalDataError
from boites.models import App, MINUTES
from . import settings


class AppTraffic(App):
    UPDATE_INTERVAL = 15 * MINUTES
    BASE_URL = 'https://maps.googleapis.com/maps/api/directions/json'

    start = models.CharField(_('Point de départ'), max_length=1024,  null=True, default=None)
    dest = models.CharField(_('Destination'), max_length=1024, null=True, default=None)
    trajectory_name = models.CharField(_('Itinéraire'), max_length=128, null=True, default=None)
    trip_duration = models.PositiveSmallIntegerField(_('Durée'), null=True, default=None)

    def update_data(self):
        params = {'origin': self.start,
                  'destination': self.dest,
                  'key': settings.GOOGLE_MAPS_API_KEY}
        r = requests.get(self.BASE_URL, params=params)
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
