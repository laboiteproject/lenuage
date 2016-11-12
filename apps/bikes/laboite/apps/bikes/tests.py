# coding: utf-8

from __future__ import unicode_literals

from datetime import timedelta
import json

from django.utils import timezone
import requests

from .models import AppBikes
from .settings import VALUES_UPDATE_INTERVAL
from .providers import get_provider

PAST = timezone.now() - timedelta(minutes=VALUES_UPDATE_INTERVAL + 1)

STAR_SEARCH_RESULTS = '''{"nhits": 2, "parameters": {"dataset": ["vls-stations-etat-tr"], "timezone": "Europe/Paris", "q": "nom:place", "rows": 10, "sort": "nom", "format": "json", "fields": ["idstation", "nom"]}, "records": [{"datasetid": "vls-stations-etat-tr", "recordid": "03bd9f7320deca7e70c171d1a1a14224c446698b", "fields": {"idstation": 24, "nom": "Place de Bretagne"}, "record_timestamp": "2016-10-21T12:22:00+02:00"}, {"datasetid": "vls-stations-etat-tr", "recordid": "b4619d5f34e51da488f9fb19ebb8e88020d78df0", "fields": {"idstation": 4, "nom": "Place Hoche"}, "record_timestamp": "2016-10-21T12:22:00+02:00"}]}'''
STAR_STATION_INFOS = '''{"nhits": 1, "parameters": {"dataset": ["vls-stations-etat-tr"], "timezone": "Europe/Paris", "q": "idstation:4", "rows": 10, "format": "json", "fields": ["nom", "nombreemplacementsactuels", "nombrevelosdisponibles", "etat"]}, "records": [{"datasetid": "vls-stations-etat-tr", "recordid": "b4619d5f34e51da488f9fb19ebb8e88020d78df0", "fields": {"etat": "En fonctionnement", "nom": "Place Hoche", "nombrevelosdisponibles": 18, "nombreemplacementsactuels": 24}, "record_timestamp": "2016-10-21T12:23:00+02:00"}]}'''
VELIB_SEARCH_RESULTS = '''{"nhits": 2, "parameters": {"dataset": ["stations-velib-disponibilites-en-temps-reel"], "timezone": "UTC", "q": "metro", "rows": 10, "format": "json", "fields": ["number", "name"]}, "records": [{"datasetid": "stations-velib-disponibilites-en-temps-reel", "recordid": "581a0aa68a4f7878ec806ea8308651c685af1c69", "fields": {"name": "08020 - METRO ROME", "number": 8020}}, {"datasetid": "stations-velib-disponibilites-en-temps-reel", "recordid": "8a856279aa389e032b5495c8de11e624423ee35c", "fields": {"name": "22401 - DE GAULLE (MALAKOFF)", "number": 22401}}]}'''
VELIB_STATION_INFOS = '''{"nhits": 1, "parameters": {"dataset": ["stations-velib-disponibilites-en-temps-reel"], "timezone": "UTC", "q": "number:8020", "rows": 10, "format": "json", "fields": ["name", "bike_stands", "available_bikes", "status"]}, "records": [{"datasetid": "stations-velib-disponibilites-en-temps-reel", "recordid": "581a0aa68a4f7878ec806ea8308651c685af1c69", "fields": {"status": "OPEN", "bike_stands": 44, "available_bikes": 7, "name": "08020 - METRO ROME"}}]}'''


class MockRequest(object):
    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data

    @property
    def ok(self):
        return self.status_code == 200


def _patch_ok(monkeypatch, result_string):
    monkeypatch.setattr(requests, 'get', lambda url, params: MockRequest(200, json.loads(result_string)))
    monkeypatch.setattr(AppBikes, 'save', lambda self: True)


def _patch_ko(monkeypatch):
    monkeypatch.setattr(requests, 'get', lambda url, params: MockRequest(500, ''))
    monkeypatch.setattr(AppBikes, 'save', lambda self: True)


def _get_stations(provider_name):
    provider = get_provider(provider_name)
    return provider.get_stations('whatever')


def _get_station_infos(provider_name):
    provider = get_provider(provider_name)
    return provider.get_station_infos('whatever')


# Common
def test_should_update():
    model = AppBikes(created_date=timezone.now(), last_activity=None)
    assert model.should_update()
    model = AppBikes(created_date=timezone.now() - timedelta(days=10), last_activity=None)
    assert model.should_update()
    model = AppBikes(created_date=timezone.now(), last_activity=timezone.now())
    assert model.should_update()
    model = AppBikes(created_date=timezone.now() - timedelta(days=10), last_activity=timezone.now() - timedelta(hours=1))
    assert model.should_update()

    model = AppBikes(created_date=timezone.now() - timedelta(seconds=30), last_activity=timezone.now())
    assert not model.should_update()
    model = AppBikes(created_date=timezone.now() - timedelta(days=10), last_activity=timezone.now())
    assert not model.should_update()


def test_not_enabled():
    model = AppBikes(created_date=PAST - timedelta(minutes=10), last_activity=PAST, enabled=False)
    assert model.get_app_dictionary() is None


# Star
def test_search_results_ok_star(monkeypatch):
    _patch_ok(monkeypatch, STAR_SEARCH_RESULTS)
    assert _get_stations('star') == [(24, 'Place de Bretagne'), (4, 'Place Hoche')]


def test_search_results_ko_star(monkeypatch):
    _patch_ko(monkeypatch)
    assert len(_get_stations('star')) == 0


def test_station_infos_ok_star(monkeypatch):
    _patch_ok(monkeypatch, STAR_STATION_INFOS)
    model = AppBikes(created_date=PAST - timedelta(minutes=10), last_activity=PAST, enabled=True, provider='star')
    assert model.get_app_dictionary() == {'provider': 'star',
                                          'station': 'Place Hoche',
                                          'slots': 24,
                                          'bikes': 18,
                                          'status': True}


def test_station_infos_ko_star(monkeypatch):
    _patch_ko(monkeypatch)
    model = AppBikes(created_date=PAST - timedelta(minutes=10), last_activity=PAST, enabled=True, provider='star')
    assert model.get_app_dictionary() is None


# Velib
def test_search_results_ok_velib(monkeypatch):
    _patch_ok(monkeypatch, VELIB_SEARCH_RESULTS)
    assert _get_stations('velib') == [(8020, '08020 - METRO ROME'), (22401, '22401 - DE GAULLE (MALAKOFF)')]


def test_search_results_ko_velib(monkeypatch):
    _patch_ko(monkeypatch)
    assert len(_get_stations('velib')) == 0


def test_station_infos_ok_velib(monkeypatch):
    _patch_ok(monkeypatch, VELIB_STATION_INFOS)
    model = AppBikes(created_date=PAST - timedelta(minutes=10), last_activity=PAST, enabled=True, provider='velib')
    assert model.get_app_dictionary() == {'provider': 'velib',
                                          'station': '08020 - METRO ROME',
                                          'slots': 44,
                                          'bikes': 7,
                                          'status': True}


def test_station_infos_ko_velib(monkeypatch):
    _patch_ko(monkeypatch)
    model = AppBikes(created_date=PAST - timedelta(minutes=10), last_activity=PAST, enabled=True, provider='velib')
    assert model.get_app_dictionary() is None
