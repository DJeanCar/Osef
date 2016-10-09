# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-09 17:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0014_auto_20161002_1056'),
        ('users', '0011_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='almacen_movement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stores.SocioMovement'),
        ),
        migrations.AddField(
            model_name='notification',
            name='store_movement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stores.Movement'),
        ),
    ]
