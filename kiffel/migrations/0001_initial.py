# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 01:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('nickname', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nickname (Namensschild)')),
                ('vorname', models.CharField(blank=True, max_length=100, null=True)),
                ('nachname', models.CharField(blank=True, max_length=100, null=True)),
                ('student', models.BooleanField(default=False)),
                ('hochschule', models.CharField(blank=True, max_length=100, null=True, verbose_name='Hochschule/Ort/Verein')),
                ('kommentar_public', models.TextField(blank=True, null=True, verbose_name='Kommentar öffentlich')),
                ('kommentar_orga', models.TextField(blank=True, null=True, verbose_name='Kommentar Orga')),
                ('anreise_geplant', models.DateTimeField(blank=True, null=True)),
                ('abreise_geplant', models.DateTimeField(blank=True, null=True)),
                ('ernaehrungsgewohnheit', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ernährungsgewohnheit')),
                ('lebensmittelunvertraeglichkeiten', models.CharField(blank=True, max_length=400, null=True, verbose_name='Lebensmittelunverträglichkeiten')),
                ('volljaehrig', models.BooleanField(default=False, verbose_name='Volljährig (über 18)')),
                ('eigener_schlafplatz', models.BooleanField(default=False, verbose_name='Hat eigenen Schlafplatz')),
                ('tshirt_groesse', models.CharField(blank=True, max_length=10, null=True, verbose_name='T-Shirt-Größe')),
                ('nickname_auf_tshirt', models.BooleanField(default=False, verbose_name='Nickname auf T-Shirt drucken')),
                ('kapuzenjacke_groesse', models.CharField(blank=True, max_length=10, null=True, verbose_name='Kapuzenjacke (evtl. Größe)')),
                ('nickname_auf_kapuzenjacke', models.BooleanField(default=False, verbose_name='Nickname auf Kapuzenjacke drucken')),
                ('weitere_tshirts', models.CharField(blank=True, max_length=100, null=True, verbose_name='Weitere T-Shirts')),
                ('interesse_theater', models.BooleanField(default=False, verbose_name='Interesse an Theaterbesuch')),
                ('interesse_esoc', models.BooleanField(default=False, verbose_name='Interesse an ESOC-Führung')),
                ('anmeldung_angelegt', models.DateTimeField(blank=True, null=True)),
                ('anmeldung_aktualisiert', models.DateTimeField(blank=True, null=True)),
                ('kommentar', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('datum_bezahlt', models.DateTimeField(blank=True, null=True, verbose_name='Tn.beitrag bezahlt')),
                ('datum_tuete_erhalten', models.DateTimeField(blank=True, null=True, verbose_name='Tüte erhalten')),
                ('datum_tshirt_erhalten', models.DateTimeField(blank=True, null=True, verbose_name='T-Shirt erhalten')),
                ('datum_teilnahmebestaetigung_erhalten', models.DateTimeField(blank=True, null=True, verbose_name='Teilnahmebestätigung erhalten')),
                ('twitter_handle', models.CharField(blank=True, max_length=100, null=True, verbose_name='Twitter-Handle')),
                ('kdv_id', models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='KDV-ID')),
                ('ist_kiffel', models.BooleanField(default=False, verbose_name='Person ist Kiffel')),
                ('ist_orga', models.BooleanField(default=False, verbose_name='Person ist Orga')),
                ('ist_helfer', models.BooleanField(default=False, verbose_name='Person ist Helfer')),
                ('ist_anonym', models.BooleanField(default=False, verbose_name='Person ist Anonym')),
                ('engel_id', models.IntegerField(blank=True, null=True)),
                ('anmeldung_id', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='E-Mail')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': (('import_persons', 'Import new persons'),),
                'verbose_name': 'Person',
                'ordering': ('nickname',),
                'verbose_name_plural': 'Personen',
            },
        ),
    ]
