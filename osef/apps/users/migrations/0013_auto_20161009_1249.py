# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-09 17:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20161009_1247'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='almacen_movement',
            new_name='socio_movement',
        ),
    ]
