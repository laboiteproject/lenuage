from datetime import timedelta

import pytest
from django.utils import timezone

from .models import App


class FakeApp(App):
    UPDATE_INTERVAL = 1

    class Meta:
        app_label = 'alarm'  # Steal name from other app to prevent errors about not existing table


@pytest.fixture
def app(boite):
    return FakeApp(boite=boite)


def test_should_update(app):
    app.created_date = timezone.now()
    app.last_activity = None
    assert app.should_update()

    app.created_date = timezone.now() - timedelta(days=10)
    app.last_activity = None
    assert app.should_update()

    app.created_date = timezone.now() - timedelta(days=10)
    app.last_activity = timezone.now() - timedelta(hours=1)
    assert app.should_update()

    app.created_date = timezone.now() - timedelta(seconds=30)
    app.last_activity = timezone.now()
    assert not app.should_update()

    app.created_date = timezone.now() - timedelta(days=10)
    app.last_activity = timezone.now()
    assert not app.should_update()

    app.created_date = timezone.now()
    app.last_activity = timezone.now()
    assert not app.should_update()
