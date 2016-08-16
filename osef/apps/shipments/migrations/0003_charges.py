# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-16 05:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0002_auto_20160816_0515'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('kind', models.CharField(choices=[('directo', 'Directo'), ('indirecto', 'Indirecto')], max_length=50)),
            ],
        ),
    ]
