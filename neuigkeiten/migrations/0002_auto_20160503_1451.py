# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-03 12:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neuigkeiten', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beitrag',
            name='published_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Veröffentlichungsdatum'),
        ),
    ]
