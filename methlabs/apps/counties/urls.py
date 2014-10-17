from django.conf.urls import patterns, include, url


urlpatterns = patterns('apps.authors.views',

    url(r'^browse/$', 'view_author_list', name="view_author_list"),


)
