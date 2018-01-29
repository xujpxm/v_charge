# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.shortcuts import render
from django.http import JsonResponse
from vpn.models import Member
from libs import member_operate

# Create your views here.


def member_create(request):
    """用户开通"""
    member_id = request.GET.get('member_id')
    member = Member.objects.get(id=member_id)
    result = member_operate.create_member(member)
    if result:
        return JsonResponse({member.username: "Successful~"})
    else:
        return JsonResponse({member.username: "Failed!!!"})


def member_enable(request):
    """用户续费"""
    member_id = request.GET.get('member_id')
    member = Member.objects.get(id=member_id)
    enable_result = member_operate.enable_member(member)
    if enable_result:
        return JsonResponse({member.username: "Enable user success!"})
    else:
        return JsonResponse({member.username: "Enable user Failed, the user is already be enabled?"})
