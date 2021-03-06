# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-21 12:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


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
                'ordering': ('titel',),
                'verbose_name_plural': 'Arbeitskreise',
                'verbose_name': 'Arbeitskreis',
            },
        ),
        migrations.CreateModel(
            name='AKTermin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kommentar', models.TextField(blank=True, verbose_name='Kommentar')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='Termin-Anfang')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='Termin-Ende')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Scheduled'), (2, 'Preferred'), (3, 'Not scheduled')])),
                ('duration', models.DurationField(verbose_name='Dauer')),
                ('constraintWeekDays', models.CharField(blank=True, max_length=255, null=True, verbose_name='An einem der Tage')),
                ('constraintBeforeTime', models.DateTimeField(blank=True, max_length=255, null=True, verbose_name='Nicht vor Datum/Zeit')),
                ('constraintAfterTime', models.DateTimeField(blank=True, max_length=255, null=True, verbose_name='Nicht nach Datum/Zeit')),
                ('constraintRooms', models.CharField(blank=True, max_length=255, null=True, verbose_name='In einem der Räume')),
                ('constraintNotParallelWithEvents', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nicht gleichzeitig mit Veranstaltung(en)')),
                ('constraintForceParallelWithEvents', models.CharField(blank=True, max_length=255, null=True, verbose_name='Gleichzeitig mit Veranstaltung(en)')),
                ('constraintBeforeEvents', models.CharField(blank=True, max_length=255, null=True, verbose_name='Gleichzeitig mit Veranstaltung(en)')),
                ('constraintAfterEvents', models.CharField(blank=True, max_length=255, null=True, verbose_name='Gleichzeitig mit Veranstaltung(en)')),
                ('ak', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oplan.AK', verbose_name='AK')),
            ],
            options={
                'verbose_name': 'AK-Termin',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50, unique=True, verbose_name='Nummer')),
                ('type', models.CharField(choices=[('SR', 'Kleingruppenraum'), ('HS', 'Hörsaal'), ('PC', 'PC-Pool'), ('LZ', 'Lernzentrum'), ('SO', 'Sonstiges')], max_length=2, verbose_name='Typ')),
                ('has_beamer', models.BooleanField(default=False, verbose_name='Beamer vorhanden?')),
                ('capacity', models.IntegerField(verbose_name='Anzahl Plätze')),
                ('lat', models.FloatField(blank=True, default=0, verbose_name='Latitude')),
                ('lng', models.FloatField(blank=True, default=0, verbose_name='Longitude')),
                ('mgmt_source', models.CharField(blank=True, max_length=20)),
                ('mgmt_id', models.CharField(blank=True, max_length=50)),
                ('mgmt_link', models.CharField(blank=True, max_length=255)),
                ('mgmt_comment', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'ordering': ['number'],
                'verbose_name_plural': 'Räume',
                'verbose_name': 'Raum',
            },
        ),
        migrations.CreateModel(
            name='RoomAvailability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='Termin-Anfang')),
                ('end_time', models.DateTimeField(verbose_name='Termin-Ende')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'OK (Reserved)'), (2, 'Blocked by other event'), (3, 'Should Request'), (4, 'Requested'), (5, 'Recommended Slot')])),
                ('kommentar', models.TextField(blank=True, verbose_name='Kommentar')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oplan.Room', verbose_name='Raum')),
            ],
            options={
                'verbose_name': 'AK-Slot',
            },
        ),
        migrations.AddField(
            model_name='aktermin',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='oplan.Room', verbose_name='Raum'),
        ),
    ]
