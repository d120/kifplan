# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-09 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiffel', '0008_kiffel_kdv_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='kiffel',
            name='ist_orga',
            field=models.BooleanField(default=False, verbose_name='Kiffel ist auch Orga'),
        ),
    ]