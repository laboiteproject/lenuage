# coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models


from boites.models import App


HOURS_CHOICES = [(v, _(v)) for v in ('{:02d}'.format(v) for v in range(24))]
MINUTES_CHOICES = [(v, _(v)) for v in ('{:02d}'.format(v) for v in range(0, 60, 5))]


class AppAlarm(App):
    heure = models.CharField(_('Heure'), help_text=_("Veuillez saisir l'heure de votre alarme"), max_length=32, default=_('00'), choices=HOURS_CHOICES)
    minutes = models.CharField(_(u'Minutes'), help_text=_('Veuillez saisir les minutes de votre alarme'), max_length=32, default=_(u"00"),choices=MINUTES_CHOICES)

    def _get_data(self):
        return {'alarm': '{}:{}'.format(self.heure, self.minutes)}

    class Meta:
        verbose_name = _('Configuration : alarme')
        verbose_name_plural = _('Configurations : alarme')
