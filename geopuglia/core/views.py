from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from ctr.models import Point, Line, Polygon, Layer

def home(request):
    """
    Main page
    """
    return render_to_response('index.html', context_instance=RequestContext(request))

def get_layers(request):
    """
    Returns the layer codes and descriptions as json
    """
    if request.is_ajax():
        if request.method == ('GET'):
            geometry_type = request.GET['geometry_type']
            if geometry_type in ('POINT', 'LINE', 'POLYGON'):
                layers = Layer.objects.filter(geometry_type=geometry_type).exclude(description__contains='simbolo')
                json = serializers.serialize('json', layers)
                return HttpResponse(json)
            else:
                return HttpResponseBadRequest('Bad request')
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

def wfs_proxy(request):
    """
    Mapserver proxy to use crossdomain Ajax requests
    """
    if request.method == ('GET'):
        url = request.GET['url']
        service = '&SERVICE=' + request.GET['service']
        version = '&VERSION=' + request.GET['version']
        req = '&REQUEST=' + request.GET['request']
        typename = '&TYPENAME=' + request.GET['typeName']
        # outputformat = '&OUTPUTFORMAT=' + request.GET['outputFormat']
        srs = '&SRS=' + request.GET['srs']
        bbox = '&BBOX=' + request.GET['bbox']
        conn = httplib2.Http()
        url = url + service + version + req + typename + srs + bbox  # + outputformat
        response, content = conn.request(url, request.method)
        return HttpResponse(content, status=int(response['status']), mimetype=response['content-type'])
