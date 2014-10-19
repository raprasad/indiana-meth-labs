from django.conf.urls import patterns, include, url



urlpatterns = patterns('apps.clanlabs.views',

    url(r'^list/august-2014/$', 'view_august_2014', name="view_august_2014"),

    url(r'^list-inefficient/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', 'view_list_by_month_inefficient', name="view_list_by_month_inefficient"),

    url(r'^list/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', 'view_list_by_month', name="view_list_by_month"),

    url(r'^list-m2m-inefficient/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', 'view_list_by_month_m2m_inefficient', name="view_list_by_month_m2m_inefficient"),

    url(r'^list-m2m/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', 'view_list_by_month_m2m', name="view_list_by_month_m2m"),

)

urlpatterns += patterns('apps.clanlabs.views_with_menu',

    url(r'^list-with-menu/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'view_list_by_month_with_menu', name="view_list_by_month_with_menu"),

)
