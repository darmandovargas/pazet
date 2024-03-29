# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-17 04:35
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('depto_codigodane', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Codigo dane')),
                ('depto_nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('depto_iso', models.CharField(max_length=10, verbose_name='ISO')),
                ('depto_delimitacion', django.contrib.gis.db.models.fields.MultiPolygonField(help_text='Delimitaci\xf3n geografica', srid=4326, verbose_name='Delimitaci\xf3n')),
                ('depto_created', models.DateTimeField(auto_now_add=True, verbose_name='Registro')),
                ('depto_updated', models.DateTimeField(auto_now=True, verbose_name='Actualizaci\xf3n')),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Departamentos',
                'db_table': 'orgtecol_departamento',
                'verbose_name': 'Departamento',
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('mun_id', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('mun_nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('mun_codigodane', models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Codigo Dane')),
                ('mun_delimitacion', django.contrib.gis.db.models.fields.MultiPolygonField(help_text='Delimitaci\xf3n geografica', srid=4326, verbose_name='Delimitaci\xf3n')),
                ('mun_created', models.DateTimeField(auto_now_add=True, verbose_name='Registro')),
                ('mun_updated', models.DateTimeField(auto_now=True, verbose_name='Actualizaci\xf3n')),
                ('depto', models.ForeignKey(db_column='depto_codigodane', on_delete=django.db.models.deletion.CASCADE, to='orgtecol.Departamento', verbose_name='Departamento')),
            ],
            options={
                'managed': True,
                'ordering': ('mun_nombre',),
                'verbose_name_plural': 'Municipios',
                'db_table': 'orgtecol_municipio',
                'verbose_name': 'Municipio',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('reg_id', models.AutoField(primary_key=True, serialize=False)),
                ('reg_nombre', models.CharField(max_length=100, unique=True, verbose_name='Regi\xf3n')),
                ('reg_delimitacion', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
                ('reg_created', models.DateTimeField(auto_now_add=True, verbose_name='Registro')),
                ('reg_updated', models.DateTimeField(auto_now=True, verbose_name='Actualizaci\xf3n')),
            ],
            options={
                'verbose_name': 'Regi\xf3n',
                'db_table': 'orgtecol_region',
                'managed': True,
                'verbose_name_plural': 'Regiones',
            },
        ),
        migrations.AddField(
            model_name='departamento',
            name='reg',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orgtecol.Region', verbose_name='Regi\xf3n'),
        ),
        migrations.AlterUniqueTogether(
            name='municipio',
            unique_together=set([('depto', 'mun_nombre')]),
        ),
        migrations.AlterUniqueTogether(
            name='departamento',
            unique_together=set([('reg', 'depto_nombre')]),
        ),
    ]
