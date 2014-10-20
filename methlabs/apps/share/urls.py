from django.conf.urls import patterns, include, url


urlpatterns = patterns('apps.share.views',

    url(r'^send-email/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'view_share_report', name="view_share_report"),

    url(r'^send-email-success/(?P<shared_info_md5>\w{32})/$', 'view_share_report_success', name="view_share_report_success"),

)


