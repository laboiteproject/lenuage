# coding: utf-8
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
        return {
            'width': 32,
            'height': 12,
            'data': [
                {
                    'type': 'bitmap',
                    'width': 8,
                    'height': 10,
                    'x': 0,
                    'y': 0,
                    'color': 2,
					'content': '0xfec2c2ce8686cececefe'
                },
                {
                    'type': 'text',
                    'width': 5 * len(str(self.likes)),
                    'height': 8,
                    'x': 8,
                    'y': 2,
                    'color': 2,
					'font': 1,
					'content': '%s' % self.likes,
                },
            ]
        }

    def update_data(self):
        graph = facebook.GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN)
        graph = graph.get_object(id=self.page_name, fields='fan_count')
        self.likes = int(graph.get('fan_count'))
        self.save()

    class Meta:
        verbose_name = _('Configuration : facebook likes')
        verbose_name_plural = _('Configurations : facebook likes')
