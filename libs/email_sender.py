# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import
import traceback
import yagmail
from django.conf import settings
from libs.logger import logger_config


logger = logger_config('mail', 'mail.log')


MAIL_SUBJECT = "VPN USER WILL OUT OF SERVICE"
MAIL_BODY = """
  VPN User will out of service, please contact administrator and recharge your account.
Otherwise vpn user will be disabled.
Thanks~
"""


def send_email(mail_addr):
    """EMAIL SENDER"""
    receivers = settings.ADMINS
    try:
        yag = yagmail.SMTP(host=settings.EMAIL_HOST,
                           user=settings.EMAIL_USER,
                           port=settings.EMAIL_PORT,
                           password=settings.EMAIL_PASSWORD)
        # 发送给租户的同时抄送管理员
        receivers.append(mail_addr)
        yag.send(to=receivers, subject=MAIL_SUBJECT, contents=MAIL_BODY)
        logger.info("Mail send success to %s" % receivers)
    except Exception:
        logger.error(traceback.format_exc())
