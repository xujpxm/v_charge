# -*- coding: utf-8 -*-
from django.conf.urls import url
from vpn import views

urlpatterns = [
    url(r'^member/create/$', views.member_create, name='member_create'),
    url(r'^member/enable/$', views.member_enable, name='member_enable'),

]
