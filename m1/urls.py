"""m1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from teacher.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url(r'^table/$', table),
	url(r'^detail/(\d{1,2})/$', detail),
	url(r'^search/$', search),
	url(r'^$',alogin),
    url(r'^main/$', main),
    url(r'^student_register/$', student_register),
    url(r'^logout/$', alogout),
    url(r'^recommend/$', recommend),
    url(r'^update/$', update),

    url(r'^index/$', index),
    url(r'^all/$', aplist),
    url(r'^all/(?P<appointID>[0-9]+)/$', ap_detail),

]
