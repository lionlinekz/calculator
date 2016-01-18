from django.conf.urls import patterns, url
from calc import views

urlpatterns = patterns('',
	    url(r'^(?P<number>[0-9]+)/add_task/', views.add_task, name='add_task'),
        url(r'^(?P<number>[0-9]+)/add_item/', views.add_item, name='add_item'),
        url(r'^(?P<number>[0-9]+)', views.index, name='index'),

)
