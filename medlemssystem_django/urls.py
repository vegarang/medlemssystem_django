from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/?$', 'core.views.home'),
    url(r'^add/?$', 'core.views.add'),
    url(r'^search/?$', 'core.views.search'),
    url(r'^valid/?$', 'core.views.valid'),
    url(r'^life/?$', 'core.views.life'),
    url(r'^all/?$', 'core.views.all'),
    url(r'^view/?$', 'core.views.view'),


    url(r'^test$', 'core.views.test'),
)

urlpatterns+=staticfiles_urlpatterns()
