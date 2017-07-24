import json
from datetime import timedelta

import pytest
from django.utils import timezone

from .models import AppMetro, requests

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
def test_failed_request(app, requests_mocker):
    with requests_mocker as m:
        m.get(AppMetro.BASE_URL, status_code=500, text='')
        assert app.get_app_dictionary() is None


@pytest.mark.django_db
def test_successful_request_no_failure(app, requests_mocker):
    with requests_mocker as m:
        m.get(AppMetro.BASE_URL, text=NO_FAILURE)
        assert app.get_app_dictionary() is None


@pytest.mark.django_db
def test_no_data_successful_request_with_failure(app, requests_mocker):
    with requests_mocker as m:
        m.get(AppMetro.BASE_URL, text=WITH_FAILURE)
        assert app.get_app_dictionary() == {'failure': True, 'recovery_time': 50}
