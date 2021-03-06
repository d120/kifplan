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
            name='GuestAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=100, verbose_name='Accountname')),
                ('password', models.CharField(max_length=100, verbose_name='Passwort')),
                ('gueltig_von', models.DateTimeField()),
                ('gueltig_bis', models.DateTimeField()),
                ('vergeben', models.BooleanField()),
                ('vorname', models.CharField(blank=True, max_length=100, null=True)),
                ('nachname', models.CharField(blank=True, max_length=100, null=True)),
                ('perso_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Personalausweisnummer')),
                ('vergeben_am', models.DateTimeField(blank=True, null=True)),
                ('vergeben_durch', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Gastaccount',
                'ordering': ('login',),
            },
        ),
    ]
