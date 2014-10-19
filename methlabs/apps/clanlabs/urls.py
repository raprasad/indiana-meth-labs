from django.conf.urls import patterns, include, url



urlpatterns = patterns('apps.clanlabs.views',

    url(r'^hello/$', 'view_hello', name="view_hello"),

    url(r'^hello2/$', 'view_hello2', name="view_hello2"),

    url(r'^browse/$', 'view_lab_list', name="view_lab_list"),

)
