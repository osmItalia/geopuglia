from django.contrib.gis.db import models


class BoundaryMeta(models.Model):
    name = models.CharField(max_length=150)
    geometry = models.MultiPolygonField(srid=32633)
    area = models.FloatField(null=True, blank=True)
    perimeter = models.FloatField(null=True, blank=True)
    objects = models.GeoManager()

    class Meta:
        abstract = True


class ConfiniRegionali(BoundaryMeta):
    pass

    def __unicode__(self):
        return '%s' % self.name


class ConfiniProvinciali(BoundaryMeta):
    code = models.CharField(max_length=10, unique=True)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.code)


class ConfiniComunali(BoundaryMeta):
    code = models.CharField(max_length=12)
    code_prov = models.CharField(max_length=6)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.code)


