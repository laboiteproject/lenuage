# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

import requests

from boites.models import App, MINUTES
from . import settings


class AppLikes(App):
    UPDATE_INTERVAL = 1 * MINUTES

    page_name = models.CharField(_('Nom de la page'), max_length=96)
    likes = models.PositiveIntegerField(_("Nombre de J'aime"), blank=True, null=True)

    def _get_data(self):
        return {'likes': self.likes}

    def update_data(self):
        url = "https://graph.facebook.com/v2.8/" + self.page_name + "?fields=fan_count&access_token=" + settings.FACEBOOK_ACCESS_TOKEN
        r = requests.get(url)
        self.likes = int(r.json().get("fan_count"))
        self.save()

    class Meta:
        verbose_name = _('Configuration : Facebook likes')
        verbose_name_plural = _('Configurations : Facebook likes')
