# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from vpn.models import Member
from libs.email_sender import send_email
from libs.member_operate import disable_member

logger = logging.getLogger('vpn')


@shared_task(name='tasks.monitor_endtime')
def monitor_endtime(username):
    """
        监控租户是否到期,可用时间小于三天发送报警邮件，到期禁用租户
    :return:
    """
    member_obj = Member.objects.get(username=username)
    end_time = member_obj.end_time
    user_mail = member_obj.email
    now = timezone.now()
    if end_time > now:
        valid_days = end_time - now
        if valid_days <= timedelta(days=3):
            # 判断可用天数是否小于三天，小于三天则发送报警邮件
            logger.info("user %s email alerting..." % username)
            send_email(user_mail)
        logger.info("user %s is in service" % username)
        return True
    # 判断是否到期，到期则禁用,返回False
    logger.info('Member %s is out of service, disabled...' %
                username)
    disable_member(username)
    return False


@shared_task(name='tasks.monitor_endtime_crontab')
def monitor_endtime_crontab():
    """
        定时监控租户的到期时间
    :return:
    """
    members = Member.objects.filter(is_enabled=True)
    for user in members:
        username = user.username
        logger.info("crontab monitor %s start" % username)
        monitor_endtime.delay(username)
        logger.info("crontab monitor %s end" % username)
    logger.info("All members is monitored by this period")
