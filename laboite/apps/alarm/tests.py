import pytest

from .models import AppAlarm, HOURS_CHOICES, MINUTES_CHOICES


def test_choices():
    assert [v for k, v in HOURS_CHOICES] == ['00', '01', '02', '03', '04', '05',
                                             '06', '07', '08', '09', '10', '11',
                                             '12', '13', '14', '15', '16', '17',
                                             '18', '19', '20', '21', '22', '23']
    assert [v for k, v  in MINUTES_CHOICES] == ['00', '05', '10', '15', '20', '25',
                                                '30', '35', '40', '45', '50', '55']


@pytest.mark.django_db
def test_app_dictionary(boite):
    alarm = AppAlarm.objects.create(heure='12', minutes='30', enabled=True, boite=boite)
    assert alarm.get_app_dictionary() == {'alarm': '12:30'}

    alarm.heure = '01'
    alarm.minutes = '05'
    alarm.save(update_fields=('heure', 'minutes'))
    assert alarm.get_app_dictionary() == {'alarm': '01:05'}

    alarm.enabled = False
    alarm.save(update_fields=('enabled',))
    assert alarm.get_app_dictionary() is None
