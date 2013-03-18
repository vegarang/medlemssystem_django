from django.conf.urls import patterns, include, url


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'medlemssystem_django.views.home', name='home'),
    # url(r'^medlemssystem_django/', include('medlemssystem_django.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^person/add$', 'core.views.add_person'),
    url(r'^person/list$', 'core.views.list_current'),
    url(r'^person/listnolife$', 'core.views.list_current_nolifetime'),
    url(r'^person/listall$', 'core.views.list_all_ever'),
    url(r'^person/listlifetime$', 'core.views.list_lifetime'),
    url(r'^person/edit$', 'core.views.edit_person'),
    url(r'^person/delete$', 'core.views.delete_person'),
    url(r'^person/search$', 'core.views.search'),
    url(r'^$', 'core.views.index'),

)
