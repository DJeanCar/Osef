# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-16 05:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shipment',
            old_name='mount',
            new_name='amount',
        ),
    ]
