# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
import traceback
import vymgmt

from vpn.models import Member

logger = logging.getLogger('vpn')


def disable_member(username):
    """
        禁用租户
    :return:
    """
    try:
        member = Member.objects.get(username=username)
        host = member.vpn_server.host
        port = member.vpn_server.port
        vyos = vymgmt.Router(address=host, user='vyos',
                             port=port)
        vyos.login()
        logger.info("VyOS login success~")
        vyos.configure()
        vyos.set(
            "vpn l2tp remote-access authentication local-users username %s disable" % username)
        vyos.commit()
        vyos.save()
        vyos.exit()
        vyos.logout()
        logger.info("VyOS config success~")
        member.is_enabled = False
        member.save()
        logger.info("user %s is disabled" % username)
        return True
    except Exception:
        logger.error(traceback.format_exc())
        return False


def enable_member(member_obj):
    """
        启用vyos用户
    :username: vyos vpn username
    :return: True or False
    """
    try:
        member = member_obj
        username = member.username
        host = member.vpn_server.host
        port = member.vpn_server.port
        vyos = vymgmt.Router(address=host, user='vyos', port=port)
        vyos.login()
        vyos.configure()
        vyos.delete(
            'vpn l2tp remote-access authentication local-users username %s disable' % username)
        vyos.commit()
        vyos.save()
        vyos.exit()
        vyos.logout()
        member.is_enabled = True
        member.save()
        logger.info('VPN User {0} is enabled'.format(username))
        return True
    except Exception:
        logger.error(traceback.format_exc())
        return False


def create_member(member_obj):
    """
        开通租户
    :return:
    """
    try:
        member = member_obj
        username = member.username
        host = member.vpn_server.host
        port = member.vpn_server.port
        password = member.password
        address = member.static_ip
        vyos = vymgmt.Router(address=host, user='vyos',
                             port=port, password='yourpassword')
        vyos.login()
        logger.info("VyOS login success~")
        vyos.configure()
        vyos.set(
            "vpn l2tp remote-access authentication local-users username %s password %s" % (username, password))
        vyos.set(
            "vpn l2tp remote-access authentication local-users username %s static-ip %s" % (username, address))
        vyos.commit()
        logger.info("VyOS configuration commit success~")
        vyos.save()
        logger.info("VyOS configuration save success~")
        vyos.exit()
        vyos.logout()
        member.is_enabled = True
        member.save()
        return True
    except Exception:
        logger.error(traceback.format_exc())
        return False
