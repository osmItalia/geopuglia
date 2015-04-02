from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from models import Layer, Point, Line, Polygon

admin.site.register(Layer, OSMGeoAdmin)
admin.site.register(Point, OSMGeoAdmin)
admin.site.register(Line, OSMGeoAdmin)
admin.site.register(Polygon, OSMGeoAdmin)