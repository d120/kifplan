# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-04 00:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiffel', '0004_auto_20160504_0223'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Benutzer kann sich einloggen'),
        ),
    ]
