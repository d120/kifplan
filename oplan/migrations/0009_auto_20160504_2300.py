# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-04 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oplan', '0008_auto_20160503_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='ak',
            name='wiki_index',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='aktermin',
            name='constraintAfterEvents',
            field=models.ManyToManyField(blank=True, help_text='Suche nach einem AK-Termin, um festzulegen, dass der AK-Termin nach den ausgewählten AK-Terminen stattfinden muss', related_name='constraint_must_be_after_this', to='oplan.AKTermin', verbose_name='Nach Veranstaltung(en)'),
        ),
        migrations.AlterField(
            model_name='aktermin',
            name='constraintBeforeEvents',
            field=models.ManyToManyField(blank=True, help_text='Suche nach einem AK-Termin, um festzulegen, dass der AK-Termin vor den ausgewählten AK-Terminen stattfinden muss', related_name='constraint_must_be_before_this', to='oplan.AKTermin', verbose_name='Vor Veranstaltung(en)'),
        ),
        migrations.AlterField(
            model_name='aktermin',
            name='constraintForceParallelWithEvents',
            field=models.ManyToManyField(blank=True, help_text='Suche nach einem AK-Termin, um festzulegen, dass der AK-Termin gleichzeitig mit den ausgewählten AK-Terminen stattfinden muss', related_name='constraint_force_parallel_with_this', to='oplan.AKTermin', verbose_name='Gleichzeitig mit Veranstaltung(en)'),
        ),
        migrations.AlterField(
            model_name='aktermin',
            name='constraintNotParallelWithEvents',
            field=models.ManyToManyField(blank=True, help_text='Suche nach einem AK-Termin, um festzulegen, dass der AK-Termin nicht gleichzeitig mit den ausgewählten AK-Terminen stattfinden kann', related_name='constraint_not_parallel_with_this', to='oplan.AKTermin', verbose_name='Nicht gleichzeitig mit Veranstaltung(en)'),
        ),
        migrations.AlterField(
            model_name='aktermin',
            name='constraintRooms',
            field=models.ManyToManyField(blank=True, help_text='Gib eine Raumnummer ein, um festzulegen, dass der AK nur in ausgewählten Räumen stattfinden kann.', related_name='aktermin_constraint_room', to='oplan.Room', verbose_name='In einem der Räume'),
        ),
    ]