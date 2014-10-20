from django.conf.urls import patterns, include, url



urlpatterns = patterns('apps.clanlabs.views',

    url(r'^list/august-2014/$', 'view_august_2014', name="view_august_2014"),

    url(r'^list-inefficient/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'view_list_by_month_inefficient', name="view_list_by_month_inefficient"),

    url(r'^list/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'view_list_by_month', name="view_list_by_month"),

    url(r'^list-m2m-inefficient/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'view_list_by_month_m2m_inefficient', name="view_list_by_month_m2m_inefficient"),

    url(r'^list-m2m/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'view_list_by_month_m2m', name="view_list_by_month_m2m"),

)

urlpatterns += patterns('apps.clanlabs.views_with_menu',

    url(r'^list-with-menu/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'view_list_by_month_with_menu', name="view_list_by_month_with_menu"),

)

urlpatterns += patterns('apps.clanlabs.views_geojson',

    url(r'^test2/$', 'view_map_test2', name="view_map_test2"),

    url(r'^geojson-data/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'view_geojson_data_by_month', name="view_geojson_data_by_month"),

    url(r'^list-by-month-map/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'view_list_by_month_with_map', name="view_list_by_month_with_map"),



)



