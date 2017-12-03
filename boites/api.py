from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404

import requests

from boites.models import Boite, PushButton, Tile


class CORSJsonResponse(JsonResponse):
    """Utility class to add CORS headers to JSONResponse"""
    def __init__(self, *args, **kwargs):
        super(CORSJsonResponse, self).__init__(*args, **kwargs)
        self['Access-Control-Allow-Origin'] = '*'


def update_activity(boite, request):
    boite.last_activity = timezone.now()
    boite.last_connection = request.META.get('REMOTE_ADDR', '')
    boite.save(update_fields=('last_activity', 'last_connection'))


def boite_json_view(request, api_key):
    boite = get_object_or_404(Boite, api_key=api_key)
    update_activity(boite, request)

    boite_tiles = Tile.objects.filter(boite=boite).order_by('id')

    tiles = []
    for tile in boite_tiles:
        tiles.append({'id': tile.id,
                      'last_activity': tile.get_last_activity()})

    json = {'id': boite.id, 'tiles': tiles}

    return CORSJsonResponse(json)


def tile_json_view(request, api_key, pk):
    boite = get_object_or_404(Boite, api_key=api_key)
    update_activity(boite, request)

    tile = get_object_or_404(Tile, pk=pk)
    return CORSJsonResponse(tile.get_data())


def trigger_pushbutton_json_view(request, api_key):
    boite = get_object_or_404(Boite, api_key=api_key)
    update_activity(boite, request)

    pushbutton = get_object_or_404(PushButton, boite=boite)

    url = settings.IFTTT_API_BASE_URL
    url += boite.api_key + '/with/key/'
    url += pushbutton.api_key + '/'

    r = requests.get(url, params={'value1': boite.name.lower()})

    return CORSJsonResponse({'status_code':r.status_code})
