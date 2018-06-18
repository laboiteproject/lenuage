# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-18 19:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboite.apps.cryptocurrency', '0003_auto_20180304_0414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appcryptocurrency',
            name='value',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8, verbose_name='Valeur'),
        ),
    ]
