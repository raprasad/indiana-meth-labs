from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^reports/', include('apps.clanlabs.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^indiana-methlabs-admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^indiana-methlabs-admin/', include(admin.site.urls)),

        
)

from tastypie.api import Api
from apps.clanlabs.api import SeizureLocationTypeResource, ManufacturingMethodResource, ClanLabReportResource

v1_api = Api(api_name='v1')
v1_api.register(SeizureLocationTypeResource())
v1_api.register(ManufacturingMethodResource())
v1_api.register(ClanLabReportResource())

urlpatterns += patterns('',
    (r'^api/', include(v1_api.urls)),   
)


# Uncomment the next line to serve media files in dev.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
