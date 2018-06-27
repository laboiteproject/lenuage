from __future__ import unicode_literals

from datetime import timedelta

import pytest
from django.utils import timezone

from .models import AppBus


DATA_OK = '''{"nhits": 3223, "parameters": {"dataset": ["tco-bus-circulation-passages-tr"], "timezone": "UTC", "rows": 2, "sort": ["-depart"], "format": "json"}, "records": [{"datasetid": "tco-bus-circulation-passages-tr", "recordid": "3d7422502a3a2479961bdcc8737b19827d471ec9", "fields": {"numerobus": 1315094584, "depart": "2017-07-22T18:03:05+00:00", "departtheorique": "2017-07-22T18:02:00+00:00", "arriveetheorique": "2017-07-22T18:02:00+00:00", "idarret": "1177", "destination": "Rennes | R\u00e9publique", "nomarret": "Beaulieu Restau U", "precision": "Applicable", "idbus": "1315094584", "idcourse": "268437493", "nomcourtligne": "64", "arrivee": "2017-07-22T18:03:05+00:00", "sens": 0, "coordonnees": [48.122317, -1.639592], "idligne": "0064"}, "geometry": {"type": "Point", "coordinates": [-1.639592, 48.122317]}, "record_timestamp": "2017-07-22T18:03:00+00:00"}, {"datasetid": "tco-bus-circulation-passages-tr", "recordid": "06b2970da15f114e27c5e3a9712311129ee22fdb", "fields": {"numerobus": 769973581, "depart": "2017-07-22T18:03:05+00:00", "departtheorique": "2017-07-22T17:58:00+00:00", "arriveetheorique": "2017-07-22T17:58:00+00:00", "idarret": "3120", "destination": "Pac\u00e9 | Saint-Gilles", "nomarret": "Touche Milon", "precision": "Applicable", "idbus": "769973581", "idcourse": "268437017", "nomcourtligne": "52", "arrivee": "2017-07-22T18:03:05+00:00", "sens": 0, "coordonnees": [48.1486, -1.785006], "idligne": "0052"}, "geometry": {"type": "Point", "coordinates": [-1.785006, 48.1486]}, "record_timestamp": "2017-07-22T18:03:00+00:00"}]}'''


@pytest.fixture
def app(boite):
    d = timezone.now() - timedelta(days=1)
    return AppBus.objects.create(created_date=d, last_activity=d, boite=boite, stop='3105', enabled=True)


def test_should_update(app):
    app.last_activity = timezone.now()
    app.save()
    assert app.route0 is None
    assert app.should_update() is True

    app.route0 = 'test'
    app.save()
    assert app.should_update() is False


def test_data_ko(app, requests_mocker, settings):
    assert app.should_update() is True
    with requests_mocker as m:
        m.get(settings.STAR_API_BASE_URL, status_code=500, text='')
        assert app.get_app_dictionary() is None


def test_data_ok(app, mocker, requests_mocker, settings):
    assert app.should_update() is True
    now = timezone.now()
    now = now.replace(year=2017, month=7, day=22, hour=20, minute=19, second=10)

    mocker.patch('laboite.apps.bus.models.timezone.now', return_value=now)

    expected_data = {
        'data': [
            {'color': 2,
             'font': 1,
             'content': "64|0' 52|1303'",
             'type': 'text',
             'width': 32,
             'height': 8,
             'x': 0,
             'y': 0}
        ],
        'height': 8,
        'width': 32
    }

    with requests_mocker as m:
        m.get(settings.STAR_API_BASE_URL, text=DATA_OK)
        result = app.get_app_dictionary()
        assert result == expected_data
