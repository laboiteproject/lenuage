from django.urls import reverse

from boites.api import boite_json_view, tile_json_view, trigger_pushbutton_json_view
from boites.models import PushButton


def test_boite_json(rf, boite):
    api_key = str(boite.api_key)
    url = reverse('boites:json', kwargs={'api_key': api_key})
    req = rf.get(url)
    response = boite_json_view(req, api_key)
    assert response.status_code == 200
    assert response['Access-Control-Allow-Origin'] == '*'


def test_tile_json(rf, boite, tile):
    api_key = str(boite.api_key)
    url = reverse('boites:tile_json', kwargs={'api_key': api_key,
                                              'pk': tile.pk})
    req = rf.get(url)
    response = tile_json_view(req, str(boite.api_key), tile.pk)
    assert response.status_code == 200
    assert response['Access-Control-Allow-Origin'] == '*'


def test_trigger_pushbutton_json(rf, boite):
    PushButton.objects.create(boite=boite)
    api_key = str(boite.api_key)
    url = reverse('boites:trigger_pushbutton', kwargs={'api_key': api_key})
    req = rf.get(url)
    response = trigger_pushbutton_json_view(req, api_key)
    assert response.status_code == 200
    assert response['Access-Control-Allow-Origin'] == '*'
