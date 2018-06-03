# coding: utf-8

from __future__ import division
from __future__ import unicode_literals

import requests
from django.conf import settings
from django.db import models
from django.utils import dateparse
from django.utils import timezone
from django.utils.translation import ugettext as _

from boites.models import App, MINUTES


class AppBus(App):
    UPDATE_INTERVAL = 1 * MINUTES

    stop = models.PositiveSmallIntegerField(_('Arrêt'), help_text=_("Veuillez saisir le nom de votre arrêt de bus"), default=None, null=True)
    route0 = models.CharField(_('Prochain bus'), max_length=4, default=None, null=True)
    departure0 = models.PositiveSmallIntegerField(_('Dans'), default=None, null=True)

    route1 = models.CharField(_('Bus suivant'), max_length=4, default=None, null=True)
    departure1 = models.PositiveSmallIntegerField(_('Dans'), default=None, null=True)

    def should_update(self):
        return super(AppBus, self).should_update() or self.route0 is None

    def update_data(self):
        params = {
            'dataset': 'tco-bus-circulation-passages-tr',
            'rows': 2,
            'apikey': settings.STAR_API_KEY,
            'sort': '-depart',
            'q': 'idarret={}'.format(self.stop)
        }

        self.route0 = None
        self.departure0 = None
        self.route1 = None
        self.departure1 = None

        r = requests.get(settings.STAR_API_BASE_URL, params=params)

        now = timezone.now()
        records = r.json().get('records')
        if records:
            records = list(records)

            try:
                self.route0 = records[0]['fields']['nomcourtligne']
                departure = dateparse.parse_datetime(records[0]['fields']['depart']) - now
                if departure.total_seconds() < 0:
                    self.departure0 = 0
                else:
                    self.departure0 = departure.seconds // 60
            except IndexError:
                self.route0 = None
                self.departure0 = None

            try:
                self.route1 = records[1]['fields']['nomcourtligne']
                departure = dateparse.parse_datetime(records[1]['fields']['depart']) - now
                self.departure1 = departure.seconds / 60
            except IndexError:
                self.route1 = None
                self.departure1 = None

        self.save()

    def _get_data(self):
        return {
            'width': 32,
            'height': 8,
            'data': [
                {
                    'type': 'text',
                    'width': 32,
                    'height': 8,
                    'x': 0,
                    'y': 0,
                    'color': 2,
					'font': 1,
                    'content':  "%s|%s' %s|%s'" % (self.route0, self.departure0, self.route1, self.departure1)
                }
            ]
        }

    class Meta:
        verbose_name = _('Configuration : bus')
        verbose_name_plural = _('Configurations : bus')
