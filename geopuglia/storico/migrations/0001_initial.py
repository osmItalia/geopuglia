# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiniComunali',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=32633)),
                ('area', models.FloatField(null=True, blank=True)),
                ('perimeter', models.FloatField(null=True, blank=True)),
                ('code', models.CharField(max_length=12)),
                ('code_prov', models.CharField(max_length=6)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ConfiniProvinciali',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=32633)),
                ('area', models.FloatField(null=True, blank=True)),
                ('perimeter', models.FloatField(null=True, blank=True)),
                ('code', models.CharField(unique=True, max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ConfiniRegionali',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=32633)),
                ('area', models.FloatField(null=True, blank=True)),
                ('perimeter', models.FloatField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
