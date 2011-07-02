from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # grade
    url(r'^', include('grade.urls', namespace='grade')),

    # django twitter
    url(r'^', include('twitterauth.urls', namespace='twitterauth')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

if 'debug_toolbar_htmltidy' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^', include('debug_toolbar_htmltidy.urls')),
    )
