# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-13 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AK',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(blank=True, max_length=400, null=True, verbose_name='Bezeichnung')),
                ('leiter', models.CharField(blank=True, max_length=400, null=True, verbose_name="Wer macht's?")),
                ('anzahl', models.CharField(blank=True, max_length=400, null=True, verbose_name='Wie viele?')),
                ('wann', models.CharField(blank=True, max_length=400, null=True, verbose_name='Wann?')),
                ('dauer', models.CharField(blank=True, max_length=400, null=True, verbose_name='Dauer?')),
                ('beschreibung', models.TextField(blank=True, null=True)),
                ('wiki_link', models.CharField(blank=True, max_length=100, null=True, verbose_name='Link zur Wikiseite')),
            ],
            options={
                'verbose_name_plural': 'Arbeitskreise',
                'verbose_name': 'Arbeitskreis',
                'ordering': ('titel',),
            },
        ),
    ]