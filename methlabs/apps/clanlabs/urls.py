from django.conf.urls import patterns, include, url


urlpatterns = patterns('apps.clanlabs.views',

    url(r'^browse/$', 'view_lab_list', name="view_lab_list"),


)
