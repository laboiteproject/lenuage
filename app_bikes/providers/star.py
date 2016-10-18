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
    def get_stations(cls):
        # Use a facet to get only name for all stations
        req = requests.get(cls.STAR_API_BASE_URL, params={'dataset': 'vls-stations-etat-tr',
                                                          'rows': 0,
                                                          'facet': 'nom',
                                                          'apikey': settings.STAR_API_KEY})
        if not req.ok:
            return ()

        return [(item['name'], item['name']) for item in req.json().get('facet_groups', [{}])[0].get('facets', ())]

    @classmethod
    def get_station_infos(cls, station_name):
        req = requests.get(cls.STAR_API_BASE_URL, params={'dataset': 'vls-stations-etat-tr',
                                                          'q': 'nom:"{}"'.format(station_name),
                                                          'apikey': settings.STAR_API_KEY})
        if not req.ok:
            return
        data = req.json()
        if not data.get('nhits', 0):
            # No matching data found
            return
        data = data['records'][0]['fields']
        return {
            'nb_stands': data['nombreemplacementsactuels'],
            'nb_available': data['nombrevelosdisponibles'],
            'status': data['etat'] == u'En fonctionnement'
        }
