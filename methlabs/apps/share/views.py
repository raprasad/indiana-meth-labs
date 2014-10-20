from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext

from apps.shared_data.forms import SharedReportRecordForm
from apps.shared_data.models import SharedReportRecord

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def email_report(request, shared_report_record):
    
    assert type(shared_report_record) is SharedReportRecord, "This is not a SharedReportRecord"
    
    subject = 'Indiana Methamphetamine Clandestine Lab Report'

    from_email = shared_report_record.from_email
    to_email = [shared_report_record.to_email]
    
    text_content = return render_to_string('share/msg_txt.txt'\
                       , dict(s=shared_report_record)\
                       , context_instance=RequestContext(request)\
                       )

    html_content = return render_to_string('share/msg_html.html'\
                      , dict(s=shared_report_record)\
                      , context_instance=RequestContext(request)\
                      )
    
    shared_report_record.full_message = html_content
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
    print ('email sent')
    
def view_share_report(request, year, month):
    
    d = {}
    selected_month = date(int(year), int(month), 1)

    d['selected_month'] = selected_month
    
    if request.POST:
        f = SharedReportRecordForm(request.POST)
        if f.is_valid():
            shared_report_record = f.save()
            email_report(shared_report_record)
            success_url = reverse('view_share_report_success'\
                                , kwargs=dict(shared_info_md5=shared_report_record.md5)\
                                )
            return HttpResponseRedirect(success_url)
        else:
            d['ERROR_FOUND']  = True
    else:
        f = SharedFileInfoForm()
    
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
    d['SUCCESS'] = True
    
    #d['FILE_PROCESS_SUCCESS'] = success
    #d['FILE_PROCESS_ERR_OR_DATA'] = msg_or_data
    
    d['share_page'] = True
    d['shared_info'] = shared_file_info
    
    return render_to_response('share/share.html'\
                            , d\
                            , context_instance=RequestContext(request))
    
