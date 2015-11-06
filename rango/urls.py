from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
            url(r'^$',views.index, name='index'),
            url(r'^login/$','django.contrib.auth.views.login'),
            url(r'^logout/$',views.logout_page, name='logout'),
            url(r'^category/(?P<category_name_slug>[^/]+)/$',views.details, name='detail'),
            url(r'^about/$',views.about, name='about'),        
            url(r'^add_category/$',views.add_category, name='add_category'),
            url(r'^category/add_page/(?P<category_name_slug>[^/]+)/$',views.add_page, name='add_page'),     
            url(r'^register/$',views.register, name='register'),
            url(r'^ajax_index/$',views.ajax_index, name='ajax_index'),
            url(r'^demo_cat/$',views.demo_cat, name='demo'),
            )