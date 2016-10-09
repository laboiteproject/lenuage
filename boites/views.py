from django.views.generic.edit import UpdateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Boite

def json_view(request, pk):
    boite = get_object_or_404(Boite, pk=pk)

    return JsonResponse(boite.get_apps_dictionary(), safe=False)

class BoiteDetailView(UpdateView):
    model = Boite
    fields = ['name']
