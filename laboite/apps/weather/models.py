# coding: utf-8

from __future__ import unicode_literals

import pyowm
from django.db import models
from django.utils.translation import ugettext_lazy as _

from boites.models import App, MINUTES
from . import settings

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
        return {'temperature_now': self.temperature_now,
                'humidity_now': self.humidity_now,
                'icon_now': self.icon_now}

    def convert_owm_icon(self, owm_icon):
        # clouds
        icon = "1"
        owm_icon = owm_icon[:3]

        # clear sky
        if owm_icon == '01':
            icon = '0'
        # rain
        elif owm_icon in ('09', '10', '11'):
            icon = '2'
        # mist
        elif owm_icon == '50':
            icon = '3'
        # snow
        elif owm_icon == '13':
            icon = '4'

        return icon

    class Meta:
        verbose_name = _('Configuration : météo')
        verbose_name_plural = _('Configurations : météo')
