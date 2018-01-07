# coding: utf-8

from __future__ import unicode_literals

import pyowm
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from boites.models import App, MINUTES

ICON_CHOICES = (
    (0, 'Temps clair'),
    (1, 'Nuages'),
    (2, 'Pluie'),
    (3, 'Brouillard'),
    (4, 'Neige'),
)


class AppWeather(App):
    UPDATE_INTERVAL = 30 * MINUTES
    city_name = models.CharField(_('Ville'), help_text=_('Veuillez saisir la ville où se trouve votre boîte'), max_length=64, default=_('Paris'))
    temperature_now = models.PositiveSmallIntegerField(_('Température actuelle'), null=True)
    humidity_now = models.PositiveSmallIntegerField(_('Humidité actuelle'), null=True)
    icon_now = models.PositiveSmallIntegerField(_('Icône'), choices=ICON_CHOICES, default=1)

    def update_data(self):
        # pyowm examples : https://github.com/csparpa/pyowm#examples
        owm = pyowm.OWM(settings.OWM_APIKEY)

        # Search for current weather in city_name
        observation = owm.weather_at_place(self.city_name)
        weather = observation.get_weather()

        # Weather details
        temperatures = weather.get_temperature('celsius')

        self.temperature_now = temperatures['temp']
        self.humidity_now = weather.get_humidity()
        self.icon_now = self.convert_owm_icon(weather.get_weather_icon_name())

        self.save()

    def _get_data(self):
        return {
            'width': 32,
            'height': 10,
            'data': [
                {
                    'type': 'icon',
                    'width': 16,
                    'height': 10,
                    'x': 0,
                    'y': 0,
                        'content': self.get_bitmap_icon(),
                },
                {
                    'type': 'text',
                    'width': 10,
                    'height': 8,
                    'x': 15,
                    'y': 2,
                    'content': '%d*' % self.temperature_now,
                },
            ]
        }

    def convert_owm_icon(self, owm_icon):
        # clouds
        icon = 1
        owm_icon = owm_icon[:2]

        # clear sky
        if owm_icon == '01':
            icon = 0
        # rain
        elif owm_icon in ('09', '10', '11'):
            icon = 2
        # mist
        elif owm_icon == '50':
            icon = 3
        # snow
        elif owm_icon == '13':
            icon = 4

        return icon

    def get_bitmap_icon(self):
        return {
            0: '0x020002004010272008801040d05810400880',
            1: '0x00000380046038104410800880087ff00000',
            2: '0x0380046038104410800880087ff02a002a00',
            3: '0x00000000fffc0000fffc0000fffc00000000',
            4: '0x2a001c0088804900ff80490088801c002a00'
        }.get(self.icon_now)

    class Meta:
        verbose_name = _('Configuration : météo')
        verbose_name_plural = _('Configurations : météo')
