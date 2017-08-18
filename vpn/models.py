# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils import timezone
from datetime import timedelta
from libs.generate_passwd import generate_pwd

# Create your models here


class BaseTimeModel(models.Model):
    created_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        abstract = True


class ClientIpPool(BaseTimeModel):
    host = models.GenericIPAddressField(
        u'服务器', protocol='ipv4')
    start_ip = models.GenericIPAddressField(
        u'开始', protocol='ipv4', unique=True)
    end_ip = models.GenericIPAddressField(u'结束', protocol='ipv4', unique=True)

    def __unicode__(self):
        return self.host

    class Meta:
        verbose_name = u'地址池'
        verbose_name_plural = u'地址池'


class Server(BaseTimeModel):
    host = models.ForeignKey(ClientIpPool, verbose_name=u'服务器地址')
    type = models.CharField(u'VPN类型', max_length=16, default='l2tp')
    version = models.CharField(
        u'服务器版本', max_length=32, default='VyOS', null=True)
    updated_time = models.DateTimeField(u'更新时间', auto_now_add=True)
    port = models.IntegerField(u'端口号', default=22)

    def __unicode__(self):
        return "%s-%s" % (self.host, self.type)

    class Meta:
        ordering = ['created_time']
        verbose_name = u'服务器'
        verbose_name_plural = u'服务器'


class Member(BaseTimeModel):
    username = models.CharField(u'用户名', max_length=128, unique=True)
    password = models.CharField(u'密码', max_length=16, default=generate_pwd(8))
    email = models.EmailField(u'邮箱', max_length=256, null=True)
    vpn_server = models.ForeignKey(Server, verbose_name=u'服务器')
    static_ip = models.GenericIPAddressField(
        u'固定地址', protocol='ipv4', unique=True)
    service_life = models.IntegerField(u'开通天数', help_text=u'单位：天')
    start_time = models.DateTimeField(u'计费开始时间', default=timezone.now)
    end_time = models.DateTimeField(
        u'计费到期时间', null=True, blank=True, help_text=u'根据开通天数自动生成')
    is_enabled = models.BooleanField(u'是否启用', default=False)

    def __unicode__(self):
        return self.username

    def generate_endtime(self):
        """
            生成到期时间函数
        :return: end_time
        """
        day_num = self.service_life
        endtime = self.start_time + timedelta(days=day_num)
        self.end_time = endtime

    def save(self, *args, **kwargs):
        self.generate_endtime()
        super(Member, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id', 'username', 'static_ip']
        verbose_name = u'租户'
        verbose_name_plural = u'租户'
