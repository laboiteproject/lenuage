# coding: utf-8
from __future__ import unicode_literals
import os

import pytest

from .models import AppTraffic


HERE = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def app(boite):
    return AppTraffic.objects.create(boite=boite)


def test_result_ok(app, requests_mocker, settings):
    with open(os.path.join(HERE, 'test_data', 'ok.json')) as f:
        with requests_mocker as m:
            m.get(settings.GOOGLE_MAPS_BASE_URL, body=f)
            ret = app.get_app_dictionary()
            assert ret['trajectory_name'] == 'Rue Réaumur'
            assert ret['trip_duration'] == 10


def test_results_ko(app, requests_mocker, settings):
    with open(os.path.join(HERE, 'test_data', 'ko.json')) as f:
        with requests_mocker as m:
            m.get(settings.GOOGLE_MAPS_BASE_URL, body=f)
            assert app.get_app_dictionary() is None
