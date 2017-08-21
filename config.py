# -*- coding: utf-8 -*-
""" Project config file for development and production env"""

from __future__ import unicode_literals, absolute_import


class Config(object):
    EMAIL_HOST = ''
    EMAIL_PORT = ''
    EMAIL_USER = ''
    EMAIL_PASSWORD = ''

    def __init__(self):
        pass


class ProductionConfig(Config):
    DEBUG = False
    DB_HOST = '192.168.1.1'
    DB_NAME = 'v_charge'
    DB_USER = 'v_charge'
    DB_PASSWORD = 'yourpass'
    DB_PORT = 3306


class DevelopmentConfig(Config):
    DE_ENGINE = 'mysql'
    DEBUG = True
    DB_HOST = '127.0.0.1'
    DB_NAME = 'v_charge'
    DB_USER = 'xujpxm'
    DB_PASSWORD = '123456'
    DB_PORT = 3306


ENV_CONFIG = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
