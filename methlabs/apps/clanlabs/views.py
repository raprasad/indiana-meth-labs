from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext

from datetime import date

from apps.clanlabs.models import SeizureLocationType, ManufacturingMethod, ClandestineLabReport


def view_august_2014(request):
    d = {}
    d['title'] = 'August 2014 Report Listing'
    d['reports'] = ClandestineLabReport.objects.filter(is_visible=True\
                                    , report_date__year=2014\
                                    , report_date__month=8)
        
    return render_to_response('labs/view_august_2014.html'\
                            , d\
                            , context_instance=RequestContext(request))


def view_list_by_month_inefficient(request, year, month):
    """Too many queries"""
    
    reports = ClandestineLabReport.objects.filter(is_visible=True\
                                        , report_date__year=year\
                                        , report_date__month=month)

    d = {}
    selected_month = date(int(year), int(month), 1)
    d['selected_month']  = selected_month
    
    d['page_title'] = '%s Report Listing' % (selected_month.strftime('%B %Y'))
    d['report_count'] = reports.count()
    d['reports'] = reports
    d['note'] = """ORM woes. Easy to use BUT
    County is a Foreign Key.  <br /> &nbsp; &nbsp;-Extra query for showing the county name.
<pre>
ClandestineLabReport.objects.filter(is_visible=True\

                    , report_date__year=year\

                    , report_date__month=month)
</pre>
    """
    
    return render_to_response('labs/view_list_by_month_fk.html'\
                            , d\
                            , context_instance=RequestContext(request))
    


def view_list_by_month(request, year, month):

    reports = ClandestineLabReport.objects.select_related('county'\
                                    ).filter(is_visible=True\
                                        , report_date__year=year\
                                        , report_date__month=month)

    d = {}
    selected_month = date(int(year), int(month), 1)
    d['selected_month']  = selected_month
    
    d['page_title'] = '%s Report Listing' % (selected_month.strftime('%B %Y'))
    d['report_count'] = reports.count()
    d['reports'] = reports
    d['note'] = """<code>select_related('county')</code> solves the extra query problem:
        <br /><br />
<pre>
<s>ClandestineLabReport.objects.filter(is_visible=True)</s>
ClandestineLabReport.objects.<b>select_related('county')</b>.filter(
                        is_visible=True    
                        , report_date__year=year
                        , report_date__month=month)
</pre>
    """
    
    
    return render_to_response('labs/view_list_by_month_fk.html'\
                            , d\
                            , context_instance=RequestContext(request))


    
def view_list_by_month_m2m_inefficient(request, year, month):
    """
    M2M causes lots of queries
    """
    
    reports = ClandestineLabReport.objects.select_related('county'\
                                    ).filter(is_visible=True\
                                        , report_date__year=year\
                                        , report_date__month=month\
                                    )

    d = {}
    selected_month = date(int(year), int(month), 1)
    
    d['selected_month']  = selected_month
    
    d['page_title'] = '%s Report Listing' % (selected_month.strftime('%B %Y'))
    d['report_count'] = reports.count()
    d['reports'] = reports
    d['note'] = """ORM woes. Easy to use BUT
    <code>seizure_location_types</code> and <code>manufacturing_methods</code>  are ManyToMany.  
        <br /> &nbsp; &nbsp;- Too many queries!!

    """
    
    return render_to_response('labs/view_list_by_month_m2m.html'\
                            , d\
                            , context_instance=RequestContext(request))



def view_list_by_month_m2m(request, year, month):
    """
    Use "prefetch_related" and make the join in python
    """ 
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
    
    d['selected_month']  = selected_month
    d['page_title'] = '%s Report Listing' % (selected_month.strftime('%B %Y'))
    d['report_count'] = reports.count()
    d['reports'] = reports
    d['note'] = """<code>prefetch_related(...)</code> solves the extra query problem:
        <br /><br />
<pre>
ClandestineLabReport.objects.select_related('county').filter(is_visible=True
                    , report_date__year=year
                    , report_date__month=month                    
                ).<b>prefetch_related</b>(
                    '<b>seizure_location_types</b>'
                    , '<b>manufacturing_methods</b>'
                )
</pre>
    """
    return render_to_response('labs/view_list_by_month_m2m.html'\
                            , d\
                            , context_instance=RequestContext(request))



