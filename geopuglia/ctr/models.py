from django.contrib.gis.db import models

from model_utils.models import TimeStampedModel

GEOMETRY_TYPE_CHOICES = (
    ('POINT', 'POINT'),
    ('LINE', 'LINE'),
    ('POLYGON', 'POLYGON'),
)


class Layer(TimeStampedModel):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)
    geometry_type = models.CharField(max_length=7, choices=GEOMETRY_TYPE_CHOICES)
    objects = models.GeoManager()

    def __unicode__(self):
        return '%s - %s' % (self.code, self.description)


class AbstractGeometry(models.Model):
    sit_layer = models.CharField(max_length=10)
    layer = models.ForeignKey(Layer, default=1)
    objects = models.GeoManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return '%s (%s)' % (self.layer.description, self.sit_layer)


class Point(AbstractGeometry):
    geometry = models.PointField(srid=32633)


class Line(AbstractGeometry):
    geometry = models.MultiLineStringField(srid=32633)
    length = models.FloatField(null=True, blank=True)


class Polygon(AbstractGeometry):
    geometry = models.MultiPolygonField(srid=32633)
    area = models.FloatField(null=True, blank=True)

