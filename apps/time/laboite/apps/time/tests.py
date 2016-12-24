from django.utils import translation, timezone

from .models import AppTime

timezone.activate('Africa/Niamey')
now = timezone.now()


def mock_now():
    return now.replace(year=2000, month=1, day=13, hour=13, minute=35, second=1)


def setup_mock(monkeypatch):
    monkeypatch.setattr(AppTime, 'save', lambda self: True)
    monkeypatch.setattr(timezone, 'now', mock_now)


def test_all(monkeypatch):
    setup_mock(monkeypatch)
    translation.activate('fr')
    app = AppTime(enabled=True, tz='Africa/Niamey')
    ret = app.get_app_dictionary()
    assert ret == {'time': '14:35', 'date': '13 jan. 2000'}
    app = AppTime(enabled=True, tz='Pacific/Pitcairn')
    ret = app.get_app_dictionary()
    assert ret == {'time': '05:35', 'date': '13 jan. 2000'}
    translation.activate('en-us')
    ret = app.get_app_dictionary()
    assert ret == {'time': '5:35 a.m.', 'date': '01/13/2000'}
