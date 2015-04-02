from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='home'),
   # url(r'^admin/', include(admin.site.urls)),
)

# ajax urls
urlpatterns += patterns('',
   url(r'^get_layers/$', 'core.views.get_layers', name='get_layers')
)

