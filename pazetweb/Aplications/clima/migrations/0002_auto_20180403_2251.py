# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-03 22:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clima', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='climaco2',
            options={'managed': True, 'ordering': ['cotwo_year'], 'verbose_name': 'CO2', 'verbose_name_plural': 'CO2s'},
        ),
    ]
