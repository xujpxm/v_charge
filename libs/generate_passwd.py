# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pwgen


def generate_pwd(number=8):
    """
        Generate radom secure password
    :return: random string for pasword
    """
    generater = pwgen.pwgen
    password = generater(number)
    return password
