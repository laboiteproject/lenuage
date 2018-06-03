# coding: utf-8
from __future__ import unicode_literals

from __future__ import unicode_literals

from datetime import timedelta
from operator import itemgetter

from django.utils import timezone
import pytest

from .models import AppBikes
from .providers import get_provider, StarProvider, VelibProvider

PAST = timezone.now() - timedelta(seconds=AppBikes.UPDATE_INTERVAL + 1)

STAR_SEARCH_RESULTS = '''{"nhits": 2, "parameters": {"dataset": ["vls-stations-etat-tr"], "timezone": "Europe/Paris", "q": "nom:place", "rows": 10, "sort": "nom", "format": "json", "fields": ["idstation", "nom"]}, "records": [{"datasetid": "vls-stations-etat-tr", "recordid": "03bd9f7320deca7e70c171d1a1a14224c446698b", "fields": {"idstation": 24, "nom": "Place de Bretagne"}, "record_timestamp": "2016-10-21T12:22:00+02:00"}, {"datasetid": "vls-stations-etat-tr", "recordid": "b4619d5f34e51da488f9fb19ebb8e88020d78df0", "fields": {"idstation": 4, "nom": "Place Hoche"}, "record_timestamp": "2016-10-21T12:22:00+02:00"}]}'''
STAR_STATION_INFOS = '''{"nhits": 1, "parameters": {"dataset": ["vls-stations-etat-tr"], "timezone": "Europe/Paris", "q": "idstation:4", "rows": 10, "format": "json", "fields": ["nom", "nombreemplacementsactuels", "nombrevelosdisponibles", "etat"]}, "records": [{"datasetid": "vls-stations-etat-tr", "recordid": "b4619d5f34e51da488f9fb19ebb8e88020d78df0", "fields": {"etat": "En fonctionnement", "nom": "Place Hoche", "nombrevelosdisponibles": 18, "nombreemplacementsactuels": 24}, "record_timestamp": "2016-10-21T12:23:00+02:00"}]}'''
VELIB_SEARCH_RESULTS = '''{"nhits": 2, "parameters": {"dataset": ["stations-velib-disponibilites-en-temps-reel"], "timezone": "UTC", "q": "metro", "rows": 10, "format": "json", "fields": ["number", "name"]}, "records": [{"datasetid": "stations-velib-disponibilites-en-temps-reel", "recordid": "581a0aa68a4f7878ec806ea8308651c685af1c69", "fields": {"name": "08020 - METRO ROME", "number": 8020}}, {"datasetid": "stations-velib-disponibilites-en-temps-reel", "recordid": "8a856279aa389e032b5495c8de11e624423ee35c", "fields": {"name": "22401 - DE GAULLE (MALAKOFF)", "number": 22401}}]}'''
VELIB_STATION_INFOS = '''{"nhits": 1, "parameters": {"dataset": ["stations-velib-disponibilites-en-temps-reel"], "timezone": "UTC", "q": "number:8020", "rows": 10, "format": "json", "fields": ["name", "bike_stands", "available_bikes", "status"]}, "records": [{"datasetid": "stations-velib-disponibilites-en-temps-reel", "recordid": "581a0aa68a4f7878ec806ea8308651c685af1c69", "fields": {"status": "OPEN", "bike_stands": 44, "available_bikes": 7, "name": "08020 - METRO ROME"}}]}'''


@pytest.fixture
def app(boite):
    return AppBikes.objects.create(boite=boite,
                                   created_date=PAST - timedelta(minutes=10),
                                   last_activity=PAST,
                                   enabled=True)


def _get_stations(provider_name):
    provider = get_provider(provider_name)
    return provider.get_stations('whatever')


def _get_station_infos(provider_name):
    provider = get_provider(provider_name)
    return provider.get_station_infos('whatever')


# Common
@pytest.mark.django_db
def test_not_enabled(app, requests_mocker, settings):
    app.enabled = False
    app.save()
    with requests_mocker as m:
        m.get(settings.STAR_API_BASE_URL, status_code=500, text='')
        assert app.get_app_dictionary() is None


# Star
def test_search_results_ok_star(requests_mocker, settings):
    with requests_mocker as m:
        m.get(settings.STAR_API_BASE_URL, text=STAR_SEARCH_RESULTS)
        assert _get_stations('star') == [(24, 'Place de Bretagne'),
                                         (4, 'Place Hoche')]


def test_search_results_ko_star(requests_mocker, settings):
    with requests_mocker as m:
        m.get(settings.STAR_API_BASE_URL, status_code=500, text='')
        assert len(_get_stations('star')) == 0


@pytest.mark.django_db
def test_station_infos_ok_star(app, requests_mocker, settings):
    app.provider = 'star'
    app.save()
    with requests_mocker as m:
        m.get(settings.STAR_API_BASE_URL, text=STAR_STATION_INFOS)
        result = app.get_app_dictionary()
        assert len(result) == 3
        assert result['height'] == 10
        assert result['width'] == 32
        result['data'].sort(key=itemgetter('type'))
        assert len(result['data']) == 2
        assert result['data'] == [{'color': 2,
                				   'font': 1,
                                   'content': '0x00c1c208c0f878eab9bd589170e',
                                   'height': 10,
                                   'type': 'bitmap',
                                   'width': 12,
                                   'x': 5,
                                   'y': 1},
                                  {'color': 2,
                				   'font': 1,
                                   'content': '18',
                                   'height': 10,
                                   'type': 'text',
                                   'width': 10,
                                   'x': 18,
                                   'y': 3}]


@pytest.mark.django_db
def test_station_infos_ko_star(app, requests_mocker, settings):
    app.provider = 'star'
    app.save()
    with requests_mocker as m:
        m.get(settings.STAR_API_BASE_URL, status_code=500, text='')
        assert app.get_app_dictionary() is None


# Velib
def test_search_results_ok_velib(requests_mocker, settings):
    with requests_mocker as m:
        m.get(settings.VELIB_API_BASE_URL, text=VELIB_SEARCH_RESULTS)
        assert _get_stations('velib') == [(8020, '08020 - METRO ROME'),
                                          (22401, '22401 - DE GAULLE (MALAKOFF)')]


def test_search_results_ko_velib(requests_mocker, settings):
    with requests_mocker as m:
        m.get(settings.VELIB_API_BASE_URL, status_code=500, text='')
        assert len(_get_stations('velib')) == 0


@pytest.mark.django_db
def test_station_infos_ok_velib(app, requests_mocker, settings):
    app.provider = 'velib'
    app.save()
    with requests_mocker as m:
        m.get(settings.VELIB_API_BASE_URL, text=VELIB_STATION_INFOS)
        result = app.get_app_dictionary()
        assert len(result) == 3
        assert result['height'] == 10
        assert result['width'] == 32
        result['data'].sort(key=itemgetter('type'))
        assert len(result['data']) == 2
        assert result['data'] == [{'color': 2,
					               'font': 1,
                                   'content': '0x00c1c208c0f878eab9bd589170e',
                                   'height': 10,
                                   'type': 'bitmap',
                                   'width': 12,
                                   'x': 5,
                                   'y': 1},
                                  {'color': 2,
                				   'font': 1,
                                   'content': '7',
                                   'height': 10,
                                   'type': 'text',
                                   'width': 10,
                                   'x': 18,
                                   'y': 3}]


@pytest.mark.django_db
def test_station_infos_ko_velib(app, requests_mocker, settings):
    app.provider = 'velib'
    app.save()
    with requests_mocker as m:
        m.get(settings.VELIB_API_BASE_URL, status_code=500, text='')
        assert app.get_app_dictionary() is None
