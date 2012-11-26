from django.conf.urls import patterns, include, url


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'medlemssystem_django.views.home', name='home'),
    # url(r'^medlemssystem_django/', include('medlemssystem_django.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^json_people$', 'core.views.get_people'),
    url(r'^json_lifetime$', 'core.views.get_lifetime'),
    url(r'^json_semester$', 'core.views.get_semesters'),
    url(r'^json_semester/(?P<semester>.*?)$', 'core.views.get_people_by_semester'),
    #url(r'^test$', 'core.views.test'),
    url(r'^test/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'core/static' }),

)
