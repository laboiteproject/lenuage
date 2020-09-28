# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-27 19:12
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boites', '0013_auto_20171211_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='boite',
            name='screen',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Écran monochrome 32×16'), (2, 'Écran bicolore 32×16')], default=1, help_text="Veuillez sélectionner l'écran qui compose votre boîte", verbose_name="Type d'écran"),
        ),
        migrations.AlterField(
            model_name='boite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur'),
        ),
        migrations.AlterField(
            model_name='pushbutton',
            name='boite',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='boites.Boite', verbose_name='Boîte'),
        ),
        migrations.AlterField(
            model_name='tile',
            name='duration',
            field=models.PositiveSmallIntegerField(default=5000, help_text='Veuillez saisir une durée durant laquelle la tuile sera affichée (en millisecondes)', verbose_name="Durée d'affichage de la tuile"),
        ),
    ]
