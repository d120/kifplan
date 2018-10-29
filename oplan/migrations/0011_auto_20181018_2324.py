# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-18 21:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oplan', '0010_auto_20160505_0052'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Track',
                'verbose_name_plural': 'Tracks',
            },
        ),
        migrations.AlterField(
            model_name='ak',
            name='leiter_personen',
            field=models.ManyToManyField(blank=True, help_text='Werden bei Zuteilung berücksichtigt', related_name='leitet_aks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ak',
            name='track',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oplan.Track'),
        ),
    ]
