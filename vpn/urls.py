# -*- coding: utf-8 -*-
from django.conf.urls import url
from vpn.views import member_create

urlpatterns = [
    url(r'^member/create/$', member_create, name='member_create'),

]
