# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-17 12:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shipments', '0004_auto_20160816_0525'),
    ]

    operations = [
        migrations.CreateModel(
            name='KindMovement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('amount', models.IntegerField()),
                ('kind_mov', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.KindMovement')),
                ('shipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shipments.Shipment')),
            ],
        ),
    ]
