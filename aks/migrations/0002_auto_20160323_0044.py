# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-22 23:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ak',
            options={'ordering': ('titel',), 'verbose_name': 'Arbeitskreis', 'verbose_name_plural': 'Arbeitskreise'},
        ),
        migrations.AddField(
            model_name='ak',
            name='beschreibung',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ak',
            name='wiki_link',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Link zur Wikiseite'),
        ),
        migrations.AlterField(
            model_name='ak',
            name='anzahl',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Wie viele?'),
        ),
        migrations.AlterField(
            model_name='ak',
            name='dauer',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Dauer?'),
        ),
        migrations.AlterField(
            model_name='ak',
            name='leiter',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name="Wer macht's?"),
        ),
        migrations.AlterField(
            model_name='ak',
            name='titel',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Bezeichnung'),
        ),
        migrations.AlterField(
            model_name='ak',
            name='wann',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Wann?'),
        ),
    ]
