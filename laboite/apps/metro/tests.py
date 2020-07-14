from datetime import timedelta

import pytest
from django.utils import timezone

from .models import AppMetro

PAST = timezone.now() - timedelta(minutes=31)
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
                    "idligne": "1001",
                    "finpanneprevue": 50
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


@pytest.fixture
def app(boite):
    return AppMetro.objects.create(boite=boite,
                                   last_activity=PAST,
                                   created_date=PAST)


@pytest.mark.django_db
def test_not_enabled(app):
    app.enabled = False
    app.save()
    assert app.get_app_dictionary() is None


@pytest.mark.django_db
def test_failed_request(app, requests_mocker, settings):
    with requests_mocker as m:
        m.get(settings.STAR_API_BASE_URL, status_code=500, text='')
        assert app.get_app_dictionary() is None


@pytest.mark.django_db
def test_successful_request_no_failure(app, requests_mocker, settings):
    expected_data = {
        'width': 32,
        'height': 8,
        'data': [
            {
                'type': 'bitmap',
                'width': 12,
                'height': 8,
                'x': 0,
                'y': 0,
                'color': 1,
                'content': '0x2401207f8924924f3cffc528'
            },
            {
                'type': 'text',
                'width': 20,
                'height': 8,
                'x': 11,
                'y': 1,
                'color': 2,
                'font': 1,
                'content': 'OK',
            },
        ]
    }
    with requests_mocker as m:
        m.get(settings.STAR_API_BASE_URL, text=NO_FAILURE)
        assert app.get_app_dictionary() == expected_data


@pytest.mark.django_db
def test_no_data_successful_request_with_failure(app, requests_mocker, settings):
    expected_data = {
        'width': 32,
        'height': 8,
        'data': [
            {
                'type': 'bitmap',
                'width': 12,
                'height': 8,
                'x': 0,
                'y': 0,
                'color': 1,
                'content': '0x2401207f8924924f3cffc528'
            },
            {
                'type': 'text',
                'width': 20,
                'height': 8,
                'x': 11,
                'y': 1,
                'color': 2,
                'font': 1,
                'content': "50'",
            },
        ]
    }
    with requests_mocker as m:
        m.get(settings.STAR_API_BASE_URL, text=WITH_FAILURE)
        assert app.get_app_dictionary() == expected_data
