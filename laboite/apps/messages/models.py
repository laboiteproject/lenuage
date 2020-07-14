# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from boites.models import App


class AppMessages(App):
    message = models.TextField(_('Message'), help_text=_('Veuillez indiquer le message pour votre boîte (max. 140 caractères)'), max_length=140, default='', blank=True)

    def _get_data(self):
        if not self.message:
            return None
        result = {
            'width': 32,
            'height': 8,
            'data': [
                {
                    'type': 'text',
                    'width': len(self.message) * 5,
                    'height': 8,
                    'x': 0,
                    'y': 1,
                    'color': 2,
					'font': 1,
					'content': '%s' % self.message,
                },
            ]
        }
        return result

    class Meta:
        verbose_name = _("Configuration : messages")
        verbose_name_plural = _("Configurations : messages")
