#!/usr/bin/env python
# coding: utf-8

import os
import sys
import glob
import logging
import inspect
import yaml

from clocwalk.libs.core.data import paths
from clocwalk.libs.core.data import logger
from clocwalk.libs.core.data import kb
from clocwalk.libs.core.data import conf
from clocwalk.libs.core.datatype_cache import AttribDictCache
from clocwalk.libs.core.datatype_cache import AttribDictHttpCache
from clocwalk.libs.core.exception import SyntaxException
from clocwalk.libs.core.exception import GenericException
from clocwalk.libs.core.update import Upgrade


def _setPluginFunctions():
    """
    Loads plugin detecting functions from script(s)
    """
    plugins = glob.glob(os.path.join(paths.PLUGINS_PATH, "*.py"))
    if not plugins:
        plugins = glob.glob(os.path.join(paths.PLUGINS_PATH, "*.pyc"))

    if not kb.pluginFunctions:
        for found in plugins:
            dirname, filename = os.path.split(found)
            dirname = os.path.abspath(dirname)

            if filename in ("__init__.py", "__init__.pyc"):
                continue

            if filename.endswith('.pyc'):
                pluginName = filename[:-4]
            else:
                pluginName = filename[:-3]

            logger.debug("loading plugin script '%s'" % pluginName)

            if dirname not in sys.path:
                sys.path.insert(0, dirname)

            try:
                module = __import__(pluginName)
            except ImportError as msg:
                raise SyntaxException("cannot import plugin script '%s' (%s)" % (pluginName, msg))

            _ = dict(inspect.getmembers(module))
            if "start" not in _:
                errMsg = "missing function 'start(**kwargs)' "
                errMsg += "in start script '%s'" % found
                raise GenericException(errMsg)
            else:
                kb.pluginFunctions.append((_["start"], _.get("__product__", pluginName)))


def setConfigFile():
    """

    :return:
    """
    if conf.config:
        if not os.path.isfile(conf.config):
            raise IOError("'{0}' file not found.".format(conf.config))
        else:
            config_file = conf.config
    else:
        config_file = paths.CONFIG_FILE
    with open(config_file) as fp:
        conf.update(yaml.load(fp, Loader=yaml.FullLoader))


def update_check(**kwargs):
    """

    :param kwargs:
    :return:
    """
    proxies = kwargs.get('proxies', None)
    force_update = kwargs.get('force_update', True)
    http_timeout = kwargs.get('http_timeout', 15)
    upgrade_interval = kwargs.get('upgrade_interval', '7d')

    # force update
    if not os.path.isfile(paths.DB_FILE) or force_update:
        up = Upgrade(
            proxies=proxies,
            upgrade_interval=upgrade_interval,
            http_timeout=http_timeout
        )
        up.start()


def setVerbosity():
    """
    This function set the verbosity of output messages.
    """

    if conf.verbose is None:
        conf.verbose = 1

    conf.verbose = int(conf.verbose)

    if conf.verbose == 0:
        logger.setLevel(logging.ERROR)
    elif conf.verbose == 1:
        logger.setLevel(logging.INFO)
    elif conf.verbose >= 2:
        logger.setLevel(logging.DEBUG)


def init():
    """
    Set attributes into both configuration and knowledge base singletons
    based upon command line and configuration file options.
    """
    setVerbosity()
    _setPluginFunctions()
    kb.cpe_cache = AttribDictCache()
    kb.http_cache = AttribDictHttpCache()
    setConfigFile()
