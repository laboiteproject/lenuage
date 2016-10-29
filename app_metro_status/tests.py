import json
import pytest
from datetime import timedelta
from django.utils import timezone

from .settings import VALUES_UPDATE_INTERVAL
from .models import AppMetroStatus, requests


PAST = timezone.now() - timedelta(minutes=VALUES_UPDATE_INTERVAL + 1)
NO_FAILURE = """
    {

        "nhits": 1,
        "parameters": {
            "dataset": [
                "tco-metro-lignes-etat-tr"
            ],
            "timezone": "UTC",
            "rows": 10,
            "format": "json",
            "facet": [
                "nomcourt"
            ]
        },
        "records": [
            {
                "datasetid": "tco-metro-lignes-etat-tr",
                "recordid": "bf9e5ed6dbbcc1ddce87e6cf366e1e8cca3ce328",
                "fields": {
                    "etat": "OK",
                    "lastupdate": "2016-10-17T19:46:54+00:00",
                    "nomcourt": "a",
                    "idligne": "1001"
                },
                "record_timestamp": "2016-10-17T19:47:00+00:00"
            }
        ],
        "facet_groups": [
            {
                "name": "nomcourt",
                "facets": [
                    {
                        "name": "a",
                        "path": "a",
                        "count": 1,
                        "state": "displayed"
                    }
                ]
            }
        ]

    }"""

WITH_FAILURE = """
    {

        "nhits": 1,
        "parameters": {
            "dataset": [
                "tco-metro-lignes-etat-tr"
            ],
            "timezone": "UTC",
            "rows": 10,
            "format": "json",
            "facet": [
                "nomcourt"
            ]
        },
        "records": [
            {
                "datasetid": "tco-metro-lignes-etat-tr",
                "recordid": "bf9e5ed6dbbcc1ddce87e6cf366e1e8cca3ce328",
                "fields": {
                    "etat": "En panne",
                    "lastupdate": "2016-10-17T19:46:54+00:00",
                    "nomcourt": "a",
                    "idligne": "1001"
                },
                "record_timestamp": "2016-10-17T19:47:00+00:00"
            }
        ],
        "facet_groups": [
            {
                "name": "nomcourt",
                "facets": [
                    {
                        "name": "a",
                        "path": "a",
                        "count": 1,
                        "state": "displayed"
                    }
                ]
            }
        ]

    }"""


class MockRequest():
    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data


def test_not_enabled():
    model = AppMetroStatus(last_activity=PAST, created_date=PAST)
    assert model.get_app_dictionary() is None


def test_no_data_failed_request(monkeypatch):
    monkeypatch.setattr(
        requests, 'get', lambda url, params: MockRequest(500, ""))
    model = AppMetroStatus(last_activity=PAST, created_date=PAST, failures="")
    assert model.get_app_dictionary() is None


def test_no_data_successful_request_no_failure(monkeypatch):
    monkeypatch.setattr(
        requests,
        'get',
        lambda url, params: MockRequest(200, json.loads(NO_FAILURE)))
    model = AppMetroStatus(last_activity=PAST, created_date=PAST, failures="")
    assert model.get_app_dictionary() is None

def test_no_data_successful_request_with_failure(monkeypatch):
    monkeypatch.setattr(
        requests,
        'get',
        lambda url, params: MockRequest(200, json.loads(WITH_FAILURE)))
    # Prevent the model from saving to the DB, we don't need it for tests.
    monkeypatch.setattr(AppMetroStatus, 'save', lambda self: True)
    model = AppMetroStatus(last_activity=PAST, created_date=PAST, failures="")
    assert model.get_app_dictionary() == [
        {'end_failure': None, 'line_name': 'a'}]


def test_should_update():
    # Last activity was more than <delay> ago: update.
    model = AppMetroStatus(last_activity=PAST, created_date=PAST, failures="")
    assert model.should_update()

    # Last activity was not far ago, don't update.
    now = timezone.now()
    model = AppMetroStatus(last_activity=now, created_date=PAST, failures="")
    assert not model.should_update()

    # Last activity was not far ago, but was just created: update.
    model = AppMetroStatus(last_activity=now, created_date=now, failures="")
    assert model.should_update()
