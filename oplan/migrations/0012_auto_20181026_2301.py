# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-26 21:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oplan', '0011_auto_20181018_2324'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ak',
            options={'ordering': ('type', 'track', 'titel'), 'verbose_name': 'Arbeitskreis', 'verbose_name_plural': 'Arbeitskreise'},
        ),
        migrations.AddField(
            model_name='ak',
            name='type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Art'),
        ),
    ]
