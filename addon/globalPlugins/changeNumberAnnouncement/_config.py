# -*- coding: UTF-8 -*-
# Copyright (C) 2019 RLarry Wang <larry.wang.801@gmail.com>
# This file is covered by the GNU General Public License.
# See the file LICENSE for more details.
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
try:
    # noinspection PyCompatibility
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
import os.path
import configobj
try:
    from configobj.validate import Validator
except ImportError:
    from validate import Validator
import globalVars
from logHandler import log

NUMBER_CONFIG_FILENAME = "changeNumberAnnouncement.ini"

numberConfig = None

_configSpec = """
number_announce = option('number', 'single_digit', 'double_digits', 'triple_digits', default='number')
"""


def load():
    global numberConfig
    if not numberConfig:
        path = os.path.join(globalVars.appArgs.configPath, NUMBER_CONFIG_FILENAME)
        numberConfig = configobj.ConfigObj(path, configspec=StringIO(_configSpec), encoding="utf-8")
        numberConfig.newlines = "\r\n"
        numberConfig.stringify = True
        val = Validator()
        ret = numberConfig.validate(val, preserve_errors=True, copy=True)
        if not ret:
            log.warning("Configuration is invalid: %s", ret)


def save():
    global numberConfig
    if not numberConfig:
        raise RuntimeError("Config is not loaded.")
    val = Validator()
    numberConfig.validate(val, copy=True)
    numberConfig.write()
