from django.conf import settings
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.gdal import SpatialReference

from ctr.models import Layer, Point, Line, Polygon
from exceptions import ImportException
from storico.models import ConfiniProvinciali, ConfiniRegionali, ConfiniComunali

# python standard libraries
import csv
import os

CTR_PROJ = """PROJCS["WGS_1984_UTM_Zone_33N",
GEOGCS["GCS_WGS_1984",
DATUM["D_WGS_1984",
SPHEROID["WGS_1984",6378137.0,298.257223563]],
PRIMEM["Greenwich",0.0],
UNIT["Degree",0.0174532925199433]],
PROJECTION["Transverse_Mercator"],
PARAMETER["False_Easting",500000.0],
PARAMETER["False_Northing",0.0],
PARAMETER["Central_Meridian",15.0],
PARAMETER["Scale_Factor",0.9996],
PARAMETER["Latitude_Of_Origin",0.0],
UNIT["Meter",1.0]]"""

STORICO_PROJ = """PROJCS["Monte_Mario_Italy_2",
GEOGCS["GCS_Monte_Mario",
DATUM["D_Monte_Mario",
SPHEROID["International_1924",6378388.0,297.0]],
PRIMEM["Greenwich",0.0],
UNIT["Degree",0.0174532925199433]],
PROJECTION["Transverse_Mercator"],
PARAMETER["False_Easting",2520000.0],
PARAMETER["False_Northing",0.0],
PARAMETER["Central_Meridian",15.0],
PARAMETER["Scale_Factor",0.9996],
PARAMETER["Latitude_Of_Origin",0.0],
UNIT["Meter",1.0]]"""


class SitImport(object):
    """ 
    Base class for the importation 
    """

    def __init__(self):
        self.ctr_projection = SpatialReference('EPSG:32633')
        self.storico_projection = SpatialReference('EPSG:3004')
        self.encoding = "utf-8"
        # set the parameters from localsettings
        self.ctr_folder = settings.HERE('..' + ls.CTR_SHP_FOLDER) + '/'
        self.storico_folder = settings.HERE('..' + ls.STORICO_SHP_FOLDER) + '/'
        self.cc = self.storico_folder + ls.CC
        self.cp = self.storico_folder + ls.CP
        self.cr = self.storico_folder + ls.CR

    def _import_ctr_layers(self, filename="ctr_layer.csv"):
        """ 
        Imports the ctr codes with relative description 
        """
        filename = ('%s%s') % (self.ctr_folder, filename)
        with open(filename, 'U') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                code = row[0]
                description = row[1]
                l = Layer(code=code, description=description)
                l.save()

    def _import_ctr_geometries(self):
        """
        Imports the ctr geometries in the database
        """
        logfile = open('ctr_import.log', 'w')
        point_mapping = {
            'sit_layer': 'LAYER',
            'geometry': 'POINT25D',
        }
        line_mapping = {
            'sit_layer': 'LAYER',
            'geometry': 'LINESTRING25D',
        }
        line_mapping2 = {
            'sit_layer': 'Layer',
            'geometry': 'LINESTRING25D',
        }
        poly_mapping = {
            'sit_layer': 'LAYER',
            'geometry': 'POLYGON25D',
        }

        flist = os.listdir(self.ctr_folder)
        for shapefile in flist:
            if 'poi.shp' in shapefile:
                try:
                    lm = LayerMapping(Point, self.ctr_folder + shapefile, point_mapping, encoding=self.encoding,
                                      source_srs=self.ctr_projection)
                    lm.save(verbose=True, strict=True)
                except ImportException:
                    logfile.writelines(shapefile + '\n')
            elif 'lin.shp' in shapefile:
                try:
                    lm = LayerMapping(Line, self.ctr_folder + shapefile, line_mapping, encoding=self.encoding,
                                      source_srs=self.ctr_projection)
                    lm.save(verbose=True, strict=True)
                except ImportException:
                    try:
                        lm = LayerMapping(Line, self.ctr_folder + shapefile, line_mapping2, encoding=self.encoding,
                                          source_srs=self.ctr_projection)
                        lm.save(verbose=True, strict=True)
                    except:
                        logfile.writelines(shapefile + '\n')
            elif 'pol.shp' in shapefile:
                try:
                    lm = LayerMapping(Polygon, self.ctr_folder + shapefile, poly_mapping, encoding=self.encoding,
                                      source_srs=self.ctr_projection)
                    lm.save(verbose=True, strict=True)
                except ImportException:
                    logfile.writelines(shapefile + '\n')
        logfile.close()

    def _fix_ctr_relations(self):
        """
        Add the relation between Point, Line and Polygon and Layer ctr models as the LayerMapping doesn't take a relation as field
        """
        layers = Layer.objects.only('code')
        for layer in layers:
            Point.objects.filter(sit_layer=layer.code).update(layer=Layer.objects.get(code=layer.code))
            Line.objects.filter(sit_layer=layer.code).update(layer=Layer.objects.get(code=layer.code))
            Polygon.objects.filter(sit_layer=layer.code).update(layer=Layer.objects.get(code=layer.code))

    def _import_boundaries(self):
        """
        Import boundaries in the database
        """
        confini_regionali_mapping = {'name': 'REGIONE',
                                     'area': 'AREA_',
                                     'perimeter': 'PERIMETER',
                                     'geometry': 'POLYGON', }

        confini_provinciali_mapping = {'name': 'PROVINCIA',
                                       'area': 'AREA_',
                                       'perimeter': 'PERIMETER',
                                       'code': 'COD',
                                       'geometry': 'POLYGON', }

        confini_comunali_mapping = {'name': 'COMUNE',
                                    'code': 'COD_COM',
                                    'code_prov': 'COD_PROV',
                                    'area': 'SHAPE_AREA',
                                    'perimeter': 'SHAPE_LEN',
                                    'geometry': 'MULTIPOLYGON', }

        lm = LayerMapping(ConfiniRegionali, self.storico_folder + ls.CR, confini_regionali_mapping,
                          encoding=self.encoding, source_srs=self.storico_projection)
        lm.save(verbose=True, strict=True)
        lm = LayerMapping(ConfiniProvinciali, self.storico_folder + ls.CP, confini_provinciali_mapping,
                          encoding=self.encoding, source_srs=self.storico_projection)
        lm.save(verbose=True, strict=True)
        lm = LayerMapping(ConfiniComunali, self.storico_folder + ls.CC, confini_comunali_mapping,
                          encoding=self.encoding, source_srs=self.storico_projection)
        lm.save(verbose=True, strict=True)

    def _calculate_length(self):
        lines = Line.objects.all()
        for line in lines:
            line.leng = line.geometry.length
            line.save()

    def _calculate_area(self):
        polygons = Polygon.objects.all()
        for polygon in polygons:
            polygon.area = polygon.geometry.area
            polygon.save()

    def ImportCtr(self):
        """Imports CTR shapefiles and build the relations with ctr layers"""
        try:
            self._import_ctr_layers()
            self._import_ctr_geometries()
            self._fix_ctr_relations()
            self._calculate_length()
            self._calculate_area()
        except:
            raise ImportException()

    def ImportBoundaries(self):
        """ Imports boundaries and build relations between province and comuni"""
        try:
            self._import_boundaries()
            self._fix_boundaries_relations()
        except:
            raise ImportException()
