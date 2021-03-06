# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-04 00:23
from __future__ import unicode_literals

from django.db import migrations, models
import kiffel.models


class Migration(migrations.Migration):

    dependencies = [
        ('kiffel', '0003_auto_20160425_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='KDVUserBarcode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, default='fubar', max_length=255, null=True, verbose_name='Barcode')),
                ('identifiable_type', models.CharField(default='User', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'kdv_user_identifiers',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ('nickname',), 'permissions': (('import_persons', 'Import new persons'), ('resetpw_person', 'Reset a persons password')), 'verbose_name': 'Person', 'verbose_name_plural': 'Personen'},
        ),
    ]
