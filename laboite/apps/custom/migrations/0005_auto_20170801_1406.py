# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-01 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboite.apps.custom', '0004_auto_20170801_0653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appcustom',
            name='bitmap0',
            field=models.TextField(blank=True, default='', max_length=1024, verbose_name='Ic\xf4ne 0'),
        ),
        migrations.AlterField(
            model_name='appcustom',
            name='bitmap1',
            field=models.TextField(blank=True, default='', max_length=1024, verbose_name='Ic\xf4ne 1'),
        ),
        migrations.AlterField(
            model_name='appcustom',
            name='bitmap2',
            field=models.TextField(blank=True, default='', max_length=1024, verbose_name='Ic\xf4ne 2'),
        ),
        migrations.AlterField(
            model_name='appcustom',
            name='bitmap3',
            field=models.TextField(blank=True, default='', max_length=1024, verbose_name='Ic\xf4ne 3'),
        ),
        migrations.AlterField(
            model_name='appcustom',
            name='bitmap4',
            field=models.TextField(blank=True, default='', max_length=1024, verbose_name='Ic\xf4ne 4'),
        ),
    ]
