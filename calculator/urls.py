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
   	url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/add_task/', views.add_task, name='add_task'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/add_item/', views.add_item, name='add_item'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/edit_task/', views.edit_task, name='edit_task'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/edit_item/', views.edit_item, name='edit_item'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/delete_task/', views.delete_task, name='delete_task'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/delete_item/', views.delete_item, name='delete_item'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/view_items/', views.view_items, name='view_items'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/view_all/', views.view_all, name='view_all'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/allocation/', views.allocation, name='allocation'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/pay_invoice/', views.pay_invoice, name='pay_invoice'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/input_quote/', views.input_quote, name='input_quote'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/payments/', views.payments, name='payments'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/add_invoice/', views.add_invoice, name='add_invoice'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/add_payment/', views.add_payment, name='add_payment'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/add_variation/', views.add_variation, name='add_variation'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/edit_invoice/', views.edit_invoice, name='edit_invoice'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/delete_invoice/', views.delete_invoice, name='delete_invoice'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/edit_payment/', views.edit_payment, name='edit_payment'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/delete_payment/', views.delete_payment, name='delete_payment'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/edit_variation/', views.edit_variation, name='edit_variation'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^add_wishlist/$', views.add_wishlist),
    url(r'^ideas/$', views.ideas),
    url(r'^jobs/$', views.jobs),
    url(r'^add_job/$', views.add_job),
    url(r'^edit_idea/$', views.edit_idea),
    url(r'^complete_idea/$', views.complete_idea),
    url(r'^delete_idea/$', views.delete_idea),
    url(r'^delete_wishlist/$', views.delete_wishlist),
    url(r'^check/$', views.check, name='check'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/pdfView/', views.pdfView, name='pdfView'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)/estimate/', views.estimate, name='estimate'),
    url(r'^job(?P<jid>[0-9]+)/(?P<number>[0-9]+)', views.index, name='index'),
    url(r'^job(?P<jid>[0-9]+)/(?P<default>\w+)', views.default), 
    url(r'^$', views.jobs),
    url(r'^', views.jobs),
# ADD THIS NEW TUPLE!
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
    )
