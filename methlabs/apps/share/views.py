from datetime import date

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from apps.share.forms import SharedReportRecordForm
from apps.share.models import SharedReportRecord



def email_report(request, shared_report_record):
    
    assert type(shared_report_record) is SharedReportRecord, "This is not a SharedReportRecord"
    
    subject = 'Indiana Methamphetamine Clandestine Lab Report'

    from_email = shared_report_record.from_email
    to_email = shared_report_record.to_email
    
    d = dict(host=request.META['HTTP_HOST']\
            , s=shared_report_record\
            )
    
    text_content = render_to_string('share/msg_txt.txt'\
                       , d\
                       , context_instance=RequestContext(request)\
                       )

    html_content = render_to_string('share/msg_html2.html'\
                      , d\
                      , context_instance=RequestContext(request)\
                      )
    
    print ('html_content', html_content)
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
    shared_report_record.full_message = html_content
    shared_report_record.save()
    
    print ('email sent')
    
def view_share_report(request, year, month):
    
    d = {}
    selected_month = date(int(year), int(month), 1)

    d['selected_month'] = selected_month
    d['page_title'] = 'Share Report for %s' % (selected_month.strftime('%B %Y'))
    
    if request.POST:
        f = SharedReportRecordForm(request.POST)
        if f.is_valid():
            shared_report_record = f.save()
            email_report(request, shared_report_record)
            success_url = reverse('view_share_report_success'\
                                , kwargs=dict(shared_info_md5=shared_report_record.md5)\
                                )
            return HttpResponseRedirect(success_url)
        else:
            print (f.errors)
            d['ERROR_FOUND']  = True
    else:
        f = SharedReportRecordForm(initial={ 'report_month' : selected_month })
    
    d['share_form'] = f
    
    return render_to_response('share/share.html'\
                            , d\
                            , context_instance=RequestContext(request))


def view_share_report_success(request, shared_info_md5):

    try:
        shared_info = SharedReportRecord.objects.get(md5=shared_info_md5)
    except SharedReportRecord.DoesNotExist:
        raise Http404('SharedReportRecord not found')
    
    d = {}
    d['EMAIL_SUCCESS'] = True
    
    d['page_title'] = 'Share Report for %s' % (shared_info.report_month.strftime('%B %Y'))
    d['selected_month'] = shared_info.report_month
    d['shared_info'] = shared_info
    
    return render_to_response('share/share.html'\
                            , d\
                            , context_instance=RequestContext(request))
    
