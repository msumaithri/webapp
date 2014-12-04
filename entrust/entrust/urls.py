from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.conf import settings


urlpatterns = patterns('',

	url(r'^$', 'entrust_app.views.home', name='home'),
    url(r'^entrust-app/', include('entrust_app.urls')),
	url(r'^admin/', include(admin.site.urls)),
)
