"""Librairie to manage daemon.
"""

from core import Log
from core import ModuleManager

import asyncio
import os
import time

name = 'MoLA'
running = True
start_time = time.time()

ROOT_PATH = '%s/' % os.sep.join(__file__.split(os.sep)[:-2])
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
    ModuleManager.start_all()
    asyncio.get_event_loop().run_until_complete(__run())


def stop():
    """Stop daemon.
    """
    Log.debug('stop deamon')
    running = False


@asyncio.coroutine
def __run():
    """Stop daemon.
    """
    try:
        while running:
            yield from asyncio.sleep(5)

    except Exception as e:
        Log.crash(e)

    __stop()


def __stop():
    """Stop daemon.
    """
    pass
