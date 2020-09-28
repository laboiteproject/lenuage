# coding: utf-8
import os

import pytest

from .models import AppTraffic

HERE = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def app(boite):
    return AppTraffic.objects.create(boite=boite)


def test_result_ok(app, requests_mocker, settings):
    expected_data = {
        'width': 32,
        'height': 16,
        'data': [
            {
                'type': 'bitmap',
                'width': 8,
                'height': 8,
                'x': 6,
                'y': 0,
                'color': 3,
                'content': '0x3c4242ffbdff42'
            },
            {
                'type': 'text',
                'width': 11,
                'height': 8,
                'x': 14,
                'y': 1,
                'color': 2,
                'font': 1,
                'content': "10'"
            },
            {
                'type': 'text',
                'width': 55,
                'height': 8,
                'x': 0,
                'y': 9,
                'color': 2,
                'font': 1,
                'content': 'Rue Réaumur',
            }
        ]
    }
    with open(os.path.join(HERE, 'test_data', 'ok.json'), 'rb') as f:
        with requests_mocker as m:
            m.get(settings.GOOGLE_MAPS_BASE_URL, body=f)
            assert app.get_app_dictionary() == expected_data


def test_results_ko(app, requests_mocker, settings):
    with open(os.path.join(HERE, 'test_data', 'ko.json'), 'rb') as f:
        with requests_mocker as m:
            m.get(settings.GOOGLE_MAPS_BASE_URL, body=f)
            assert app.get_app_dictionary() is None
