from django.conf.urls import patterns, include, url


urlpatterns = patterns('apps.shared.views',

    url(r'^share-data/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'view_share_report', name="view_share_report"),

    url(r'^upload-success/(?P<shared_info_md5>\w{32})/$', 'view_share_report_success', name="view_share_report_success"),

)


