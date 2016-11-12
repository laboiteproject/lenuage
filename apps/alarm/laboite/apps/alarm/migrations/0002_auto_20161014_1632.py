# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-14 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboite.apps.alarm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appalarm',
            name='alarm2',
        ),
        migrations.RemoveField(
            model_name='appalarm',
            name='alarm3',
        ),
        migrations.AddField(
            model_name='appalarm',
            name='heure',
            field=models.CharField(choices=[('00', '00'), ('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23')], default='00', help_text="Veuillez saisir l'heure de votre alarme", max_length=32, verbose_name='Heure'),
        ),
        migrations.AddField(
            model_name='appalarm',
            name='minutes',
            field=models.CharField(choices=[('00', '00'), ('05', '05'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'), ('40', '40'), ('45', '45'), ('50', '50'), ('55', '55')], default='00', help_text='Veuillez saisir les minutes de votre alarme', max_length=32, verbose_name='Minutes'),
        ),
    ]
