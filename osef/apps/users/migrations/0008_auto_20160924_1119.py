# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-24 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='socio',
        ),
        migrations.AlterField(
            model_name='account',
            name='currency',
            field=models.CharField(choices=[('usd', 'Dólares'), ('mxn', 'Pesos mexicanos')], max_length=10),
        ),
    ]
