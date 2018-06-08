# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from jsonpath_ng import jsonpath, parse

from boites.models import App, MINUTES

import requests


class AppData(App):
    UPDATE_INTERVAL = 1 * MINUTES

    UPDATE_INTERVAL_CHOICES = (
        (1, _('Toutes les minutes')),
        (15, _('Tous les quarts d\'heure')),
        (30, _('Toutes les demi-heures')),
        (60, _('Toutes les heures')),
        (24*60, _('Tous les jours')),
    )

    url = models.TextField(_('URL de la ressource JSON'), help_text=_("Veuillez indiquer l'adresse de la ressource que vous souhaitez atteindre"), default='http://api.tom.tools/hits', null=False, blank=False)
    json_path = models.CharField(_("Chemin de l'élément JSON (JSON Path)"), help_text=_("Veuillez indiquer le chemin de l'élément json (exemple: articles[0].title)"), max_length=64, null=False, blank=False)
    json = models.TextField(_("Dernière version de la ressource JSON"), null=True, blank=True)
    data = models.CharField(_("Chemin de l'élément JSON (JSON Path)"), max_length=32)

    def _get_data(self):
        scrolling = True if len(self.data.strip()) > 6 else False
        return {
            'width': 32,
            'height': 8,
            'data': [
                {
                    'type': 'text',
                    'width': self.data.strip() * 5,
                    'height': 8,
                    'x': 11,
                    'y': 1,
                    'content':  '%s' % self.data.strip(),
                    'scrolling': scrolling,
                },
            ]
        }

    def update_data(self):
        url = self.url
        headers = {'content-type': 'application/json'}
        r = requests.get(url, headers=headers)

        self.json = r.json()

        if self.json:
            jsonpath_expr = parse(self.json_path)
            match = jsonpath_expr.find(self.json).pop()
            self.data = match.value
            self.save()

    class Meta:
        verbose_name = _('Configuration : données')
        verbose_name_plural = _('Configurations : données')
