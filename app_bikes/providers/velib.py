# coding: utf-8

import requests
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _L

from . import base
from .. import settings


class VelibProvider(base.BaseProvider):
    VELIB_BASE_URL = 'http://opendata.paris.fr/api/records/1.0/search'

    verbose_name = _L(u"Vélib' - Paris")

    @classmethod
    def get_stations(cls, query):
        if query.isdigit():
            query = 'name:{query} OR number:{query}'.format(query=query)
        else:
            # As number is an int in the API it raises an error otherwise
            query = 'name:{}'.format(query)
        req = requests.get(cls.VELIB_BASE_URL, params={'apikey': settings.VELIB_API_KEY,
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
        req = requests.get(cls.VELIB_BASE_URL, params={'apikey': settings.VELIB_API_KEY,
                                                       'dataset': 'stations-velib-disponibilites-en-temps-reel',
                                                       'fields': 'name,bike_stands,available_bikes,status',
                                                       'q': 'number:"{}"'.format(station_id),
                                                       'timezone': timezone.get_current_timezone_name()})
        if not req.ok:
            return
        data = req.json()
        if not data.get('nhits', 0):
            # No matching data found
            return
        data = data['records'][0]['fields']
        return {
            'station': data['name'],
            'slots': data['bike_stands'],
            'bikes': data['available_bikes'],
            'status': data['status'] == u'OPEN'
        }
