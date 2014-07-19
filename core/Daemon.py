"""Librairie to manage daemon.
"""

from core import Log
from core import ModuleManager

import asyncio
import os
import time

name = 'MoLA'
start_time = time.time()
ROOT_PATH = '%s/' % os.sep.join(__file__.split(os.sep)[:-2])
CONFIGS_PATH = '%sconfigs/' % ROOT_PATH
MODULES_PATH = '%smodules/' % ROOT_PATH


def restart():
    """Restart daemon.
    """
    stop(name)
    #start(name) todo start new aplication


def start():
    """Start daemon.
    """
    Log.init()
    ModuleManager.init_all()
    ModuleManager.load_all()
    ModuleManager.start_all()

    asyncio.get_event_loop().run_forever()


def stop():
    """Stop daemon.
    """
    Log.debug('stop deamon')
    asyncio.get_event_loop().stop()


def __stop():
    """Stop daemon.
    """
    ModuleManager.stop_all()
