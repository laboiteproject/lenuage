# coding: utf-8

from __future__ import unicode_literals

import requests
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from . import base


class VelibProvider(base.BaseProvider):
    verbose_name = _("Vélib' - Paris")

    @classmethod
    def get_stations(cls, query):
        if query.isdigit():
            query = 'name:{query} OR number:{query}'.format(query=query)
        else:
            # Querying number with a string value raises an error, we remove this field
            query = 'name:{}'.format(query)
        req = requests.get(settings.VELIB_API_BASE_URL,
                           params={'apikey': settings.VELIB_API_KEY,
                                   'dataset': 'stations-velib-disponibilites-en-temps-reel',
                                   'fields': 'number,name',
                                   'q': query,
                                   #'sort': 'name',  Seems to create an error 2016-10-21
                                   'timezone': timezone.get_current_timezone_name()})
        if not req.ok:
            return ()
        data = req.json()
        if not data.get('nhits', 0):
            # No matching data found
            return ()

        return [(item['fields']['number'], item['fields']['name']) for item in data.get('records', [])]

    @classmethod
    def get_station_infos(cls, station_id):
        req = requests.get(settings.VELIB_API_BASE_URL,
                           params={'apikey': settings.VELIB_API_KEY,
                                   'dataset': 'stations-velib-disponibilites-en-temps-reel',
                                   'fields': 'name,bike_stands,available_bikes,status',
                                   'q': 'number:"{}"'.format(station_id),
                                   'timezone': timezone.get_current_timezone_name()})
        if not req.ok:
            return None
        data = req.json()
        if not data.get('nhits', 0):
            # No matching data found
            return None
        data = data['records'][0]['fields']
        return {
            'station': data['name'],
            'slots': data['bike_stands'],
            'bikes': data['available_bikes'],
            'status': data['status'] == 'OPEN'
        }
