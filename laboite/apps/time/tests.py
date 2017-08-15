from django.utils import translation, timezone

from .models import AppTime


def test_all(boite, mocker):
    timezone.activate('Africa/Niamey')
    now = timezone.now()
    now = now.replace(year=2000, month=1, day=13, hour=13, minute=35, second=1)
    mocker.patch('laboite.apps.time.models.timezone.now', return_value=now)

    translation.activate('fr')

    app = AppTime.objects.create(boite=boite,
                                 enabled=True,
                                 tz='Africa/Niamey')
    assert app.get_app_dictionary() == {'time': '14:35',
                                        'date': '13 jan. 2000'}

    app.tz = 'Pacific/Pitcairn'
    app.save()
    assert app.get_app_dictionary() == {'time': '05:35',
                                        'date': '13 jan. 2000'}

    translation.activate('en-us')
    assert app.get_app_dictionary() == {'time': '5:35 a.m.',
                                        'date': '01/13/2000'}
