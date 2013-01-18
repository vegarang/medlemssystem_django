from django.conf.urls import patterns, include, url


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'medlemssystem_django.views.home', name='home'),
    # url(r'^medlemssystem_django/', include('medlemssystem_django.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^person/add$', 'core.views.add_person'),
    url(r'^person/list$', 'core.views.list_person'),
)
