from __future__ import unicode_literals

from django.utils import translation, timezone

from .models import AppTime


def test_all(boite, mocker):
    timezone.activate('Africa/Niamey')
    now = timezone.now()
    now = now.replace(year=2000, month=1, day=13, hour=13, minute=35, second=1)
    mocker.patch('laboite.apps.time.models.timezone.now', return_value=now)

    translation.activate('fr')

    with mocker.patch('laboite.apps.time.models.AppTime.should_update',
                      return_value=True):  # Force update
        app = AppTime.objects.create(boite=boite,
                                     enabled=True,
                                     tz='Africa/Niamey')
        result = app.get_app_dictionary()
        assert len(result) == 3
        assert result['data'] == [{'type': 'text',
                                   'width': 25,
                                   'height': 8,
                                   'x': 4,
                                   'y': 1,
                                   'color': 2,
                                   'font': 1,
                                   'content': '14:35'}]
        assert result['height'] == 8
        assert result['width'] == 32

        app.tz = 'Pacific/Pitcairn'
        app.save()
        result = app.get_app_dictionary()
        assert len(result) == 3
        assert result['data'] == [{'type': 'text',
                                   'width': 25,
                                   'height': 8,
                                   'x': 4,
                                   'y': 1,
                                   'color': 2,
                                   'font': 1,
                                   'content': '05:35'}]
        assert result['height'] == 8
        assert result['width'] == 32

        translation.activate('en-us')
        result = app.get_app_dictionary()
        assert len(result) == 3
        assert result['data'] == [{'type': 'text',
                                   'width': 25,
                                   'height': 8,
                                   'x': 4,
                                   'y': 1,
                                   'color': 2,
                                   'font': 1,
                                   'content': '5:35 a.m.'}]
        assert result['height'] == 8
        assert result['width'] == 32
