# coding: utf-8

import requests
from django.utils.translation import ugettext as _

from . import base
from .. import settings


class StarProvider(base.BaseProvider):
    STAR_API_BASE_URL = "https://data.explore.star.fr/api/records/1.0/search"

    STAR_API_URL = "{}search?dataset=vls-stations-etat-tr&facet=nom&apikey={}".format(STAR_API_BASE_URL, settings.STAR_API_KEY)

    nice_name = _(u'Star - Rennes')

    @classmethod
    def get_stations(cls, nom):
        # Use a facet to get only name for all stations
        req = requests.get(cls.STAR_API_BASE_URL, params={'dataset': 'vls-stations-etat-tr',
                                                          'q': 'nom:{}'.format(nom),
                                                          'fields': 'idstation,nom',
                                                          'apikey': settings.STAR_API_KEY})
        if not req.ok:
            return ()
        data = req.json()
        if not data.get('nhits', 0):
            # No matching data found
            return ()

        return [(item['idstation'], item['name']) for item in data.get('records', [])]

    @classmethod
    def get_station_infos(cls, station_id):
        req = requests.get(cls.STAR_API_BASE_URL, params={'dataset': 'vls-stations-etat-tr',
                                                          'q': 'idstation:"{}"'.format(station_id),
                                                          'fields': 'nom,nombreemplacementsactuels,nombrevelosdisponibles,etat',
                                                          'apikey': settings.STAR_API_KEY})
        if not req.ok:
            return
        data = req.json()
        if not data.get('nhits', 0):
            # No matching data found
            return
        data = data['records'][0]['fields']
        return {
            'station': data['nom'],
            'slots': data['nombreemplacementsactuels'],
            'bikes': data['nombrevelosdisponibles'],
            'status': data['etat'] == u'En fonctionnement'
        }
