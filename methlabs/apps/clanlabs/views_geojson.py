from datetime import date, datetime
import json

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.db.models import query

from geojson import Feature, Point, FeatureCollection

from apps.clanlabs.models import SeizureLocationType, ManufacturingMethod, ClandestineLabReport

def view_map_test2(request):
    return render_to_response('maps/test2.html'\
                             , {}\
                             , context_instance=RequestContext(request))
    
    
    
def geo_format(report):
    r = report
    if not (r.lat_position and r.lng_position):
        return None
    #point = Point( (float(r.lat_position), float(r.lng_position) ))
    point = Point( (float(r.lng_position), float(r.lat_position) ))
    f = Feature(geometry=point\
                , id=r.id\
                , properties=dict(case_number=r.case_number\
                                , report_date=r.report_date.strftime('%m/%d/%Y')\
                                )\
                )
    return f

def create_feature_collection(reports):
    """
    Transform queryset of ClandestineLabReport into JSON FeatureCollection
    """
    assert type(reports) is query.QuerySet, "Must be a Queryset"
    
    feature_list = [ geo_format(r) for r in reports if r.lat_position and r.lng_position]

    feature_collection = FeatureCollection(feature_list)  
    
    return json.dumps(feature_collection)
    
    
def view_geojson_data_by_month(request, year, month):

    # report query
    reports = ClandestineLabReport.objects.select_related('county'\
                                    ).filter(is_visible=True\
                                        , report_date__year=year\
                                        , report_date__month=month\
                                    ).prefetch_related(\
                                        'seizure_location_types'\
                                        , 'manufacturing_methods'\
                                    )
    

    #feature_list = [ geo_format(r) for r in reports if r.lat_position and r.lng_position]
    
    #feature_collection = FeatureCollection(feature_list)  
    
    return HttpResponse(create_feature_collection(reports), content_type="application/json")
 