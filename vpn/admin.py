# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from django.http import JsonResponse
from vpn.models import Server, Member, ClientIpPool
from libs.member_operate import create_member

# Register your models here.


class ClientIpPoolAdmin(admin.ModelAdmin):
    list_display = ['host', 'start_ip', 'end_ip', 'created_time']


class ServerAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'type',
                    'version', 'created_time', 'updated_time']
    list_filter = ['type', 'version']
    search_fields = ['host', 'type', 'version']


class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'static_ip', 'start_time',
                    'service_life', 'end_time', 'create_user', 'is_enabled']
    list_filter = ['service_life', 'is_enabled']
    search_fields = ['username', 'created_time', 'updated_time', 'end_time']

    def create_user(self, obj):
        """
            创建vpn 用户
        """
        return u'<a href="/vpn/member/create?member_id=%s">开通</a>' % obj.id
    create_user.short_description = u'操作'
    create_user.allow_tags = True

    def member_action(self, request, queryset):
        """
            定义用户动作
        """
        result_json = {}
        members = queryset
        for member in members:
            result = create_member(member)
            if result:
                result_json[member] = u"开通成功"
            else:
                result_json[member] = u"开通失败"
        return JsonResponse(result_json)

    member_action.short_description = u'批量开通所选租户'

    actions = ['member_action']


admin.site.register(Server, ServerAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(ClientIpPool, ClientIpPoolAdmin)
