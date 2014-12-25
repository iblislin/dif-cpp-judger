from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', '_.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'center.views.index', name='index'),
    url(r'^auth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^center/', include('center.urls', namespace='center')),
)


if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()
