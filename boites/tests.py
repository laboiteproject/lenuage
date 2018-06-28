from datetime import timedelta

import pytest
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import App, Tile, TileApp
from laboite.apps.time.models import AppTime


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


def test_get_tiles(boite):
    # Create two tiles
    tile1 = Tile.objects.create(boite=boite)
    tile2 = Tile.objects.create(boite=boite)
    # Create an app and assign it to tile 1
    app_time = AppTime.objects.create(boite=boite, tz='Europe/Paris')
    content_type = ContentType.objects.get(app_label="laboite.apps.time",
                                           model="apptime")
    tile_app_1 = TileApp.objects.create(tile=tile1, object_id=app_time.id,
                                        content_type=content_type)
    # Only tile 1 is returned
    tiles = boite.get_tiles()
    assert len(tiles) == 1
    assert tiles.first().pk == tile_app_1.pk

    # Add it in tile 2
    tile_app_2 = TileApp.objects.create(tile=tile2, object_id=app_time.id,
                                        content_type=content_type)
    # Both are returned
    tiles = boite.get_tiles()
    assert len(tiles) == 2
    assert [tile.pk for tile in tiles] == [tile_app_1.pk, tile_app_2.pk]
