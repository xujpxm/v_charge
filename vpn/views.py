# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.shortcuts import render
from django.http import JsonResponse
from vpn.models import Member
from libs.member_operate import create_member

# Create your views here.


def member_create(request):
    member_id = request.GET.get('member_id')
    member = Member.objects.get(id=member_id)
    result = create_member(member)
    if result:
        return JsonResponse({member.username: "Successful~"})
    else:
        return JsonResponse({member.username: "Failed!!!"})
