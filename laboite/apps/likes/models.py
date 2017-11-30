# coding: utf-8

from __future__ import unicode_literals

import facebook
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from boites.models import App, MINUTES


class AppLikes(App):
    UPDATE_INTERVAL = 2 * MINUTES

    page_name = models.CharField(_('Nom de la page'), max_length=96)
    likes = models.PositiveIntegerField(_("Nombre de J'aime"), blank=True, null=True)

    def _get_data(self):
        return {'likes': self.likes}

    def update_data(self):
        graph = facebook.GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN)
        graph = graph.get_object(id=self.page_name, fields='fan_count')
        self.likes = int(graph.get('fan_count'))
        self.save()

    class Meta:
        verbose_name = _('Configuration : facebook likes')
        verbose_name_plural = _('Configurations : facebook likes')
