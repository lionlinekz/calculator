from django.conf.urls import patterns, include, url
from django.contrib import admin
from calc import views
from django.conf import settings # New Import
from django.conf.urls.static import static # New Import



# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'calculator.views.home', name='home'),
    # url(r'^calculator/', include('calculator.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
   	url(r'^(?P<number>[0-9]+)/add_task/', views.add_task, name='add_task'),
    url(r'^(?P<number>[0-9]+)/add_item/', views.add_item, name='add_item'),
    url(r'^(?P<number>[0-9]+)/edit_task/', views.edit_task, name='edit_task'),
    url(r'^(?P<number>[0-9]+)/edit_item/', views.edit_item, name='edit_item'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^(?P<number>[0-9]+)/pdfView/', views.pdfView, name='pdfView'),
    url(r'^(?P<number>[0-9]+)/estimate/', views.estimate, name='estimate'),
    url(r'^(?P<number>[0-9]+)', views.index, name='index'),
    url(r'^(?P<default>\w+)', views.default), 
    url(r'^$', views.start),
# ADD THIS NEW TUPLE!
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
    )
