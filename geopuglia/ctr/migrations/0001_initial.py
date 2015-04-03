# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('description', models.CharField(max_length=255)),
                ('geometry_type', models.CharField(max_length=7, choices=[(b'POINT', b'POINT'), (b'LINE', b'LINE'), (b'POLYGON', b'POLYGON')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sit_layer', models.CharField(max_length=10)),
                ('geometry', django.contrib.gis.db.models.fields.MultiLineStringField(srid=32633)),
                ('length', models.FloatField(null=True, blank=True)),
                ('layer', models.ForeignKey(default=1, to='ctr.Layer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sit_layer', models.CharField(max_length=10)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=32633)),
                ('layer', models.ForeignKey(default=1, to='ctr.Layer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Polygon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sit_layer', models.CharField(max_length=10)),
                ('geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=32633)),
                ('area', models.FloatField(null=True, blank=True)),
                ('layer', models.ForeignKey(default=1, to='ctr.Layer')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
