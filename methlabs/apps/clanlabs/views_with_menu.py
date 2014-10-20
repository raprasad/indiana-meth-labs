from datetime import date, datetime

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext

from django.db import connection
from django.db.models import Count

from apps.clanlabs.models import SeizureLocationType, ManufacturingMethod, ClandestineLabReport



def get_month_menu_info(year):
    # Retrieve month information for year, only include months with incidents    
    #
    #   List of month string and incident count:
    #       [(u'2013-09-01', 25), (u'2013-10-01', 107)
    #
    truncate_date = connection.ops.date_trunc_sql('month','report_date')
    month_menu_info = ClandestineLabReport.objects.filter(\
                                is_visible=True
                                , report_date__year=year\
                            ).extra({'report_month':truncate_date}\
                            ).values_list('report_month'\
                            ).annotate(\
                                    Count('pk')\
                            ).order_by('report_month')

    # Format month information
    #   convert: [(u'2013-09-01', 25), (u'2013-10-01', 107)
    #       to: [(datetime.date(2013, 9, 1), 25), (datetime.date(2013, 10, 1), 107), 
    #
    month_menu_info = [ (datetime.strptime(mm[0], '%Y-%m-%d').date(), mm[1]) \
                        for mm in month_menu_info ]

    return month_menu_info
    
def view_list_by_month_with_menu(request, year, month):

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
    selected_month = date(int(year), int(month), 1)
    d['page_title'] = '%s Reports' % (selected_month.strftime('%B %Y'))
    d['report_count'] = reports.count()
    d['reports'] = reports
    d['month_menu'] = get_month_menu_info(year)
    d['year_menu'] = ClandestineLabReport.objects.filter(is_visible=True\
                                        ).dates('report_date', 'year')
    d['selected_month']  = selected_month
    
    return render_to_response('labs/view_list_by_month_with_menu.html'\
                            , d\
                            , context_instance=RequestContext(request))

