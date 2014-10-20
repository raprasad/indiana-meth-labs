from datetime import date, datetime
import json

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.db.models import query

from geojson import Feature, Point, FeatureCollection

from apps.clanlabs.models import SeizureLocationType, ManufacturingMethod, ClandestineLabReport

from apps.clanlabs.views_with_menu import get_month_menu_info

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
                                , address=r.address\
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

    return HttpResponse(create_feature_collection(reports), content_type="application/json")


def view_homepage(request):
    
    latest_report = ClandestineLabReport.objects.filter(is_visible=True).last()
    if latest_report is not None:
        selected_month = latest_report.report_date
    else:  
        selected_month = date.today()
    
    homepage_url = reverse('view_list_by_month_with_map'\
                , kwargs={ 'year' : selected_month.year\
                          , 'month' : selected_month.month })

    return HttpResponseRedirect(homepage_url)
    
    
def view_list_by_month_with_map(request, year, month):
    
    # report query
    reports = ClandestineLabReport.objects.select_related('county'\
                                    ).filter(is_visible=True\
                                        , report_date__year=year\
                                        , report_date__month=month\
                                    ).prefetch_related(\
                                        'seizure_location_types'\
                                        , 'manufacturing_methods'\
                                    )


    d = {}
    
    # create selected month
    selected_month = date(int(year), int(month), 1)
    
    
    d['page_title'] = '%s Reports' % (selected_month.strftime('%B %Y'))

    # report counts, mappable count, unmappable count
    d['report_count'] = reports.count()
    d['report_count_mappable'] = reports.exclude(lat_position=None).count()
    d['report_count_unmappable'] = d['report_count']- d['report_count_mappable']

    # reports
    d['reports'] = reports

    # top menus
    #d['month_menu'] = get_month_menu_info(year)
    d['month_menu'] =  ClandestineLabReport.objects.filter(is_visible=True\
                                            , report_date__year=year\
                                        ).dates('report_date', 'month')
    
    d['year_menu'] = ClandestineLabReport.objects.filter(is_visible=True\
                                        ).dates('report_date', 'year')
    d['selected_month']  = selected_month
    
    return render_to_response('maps/view_list_by_month_with_map.html'\
                            , d\
                            , context_instance=RequestContext(request))

