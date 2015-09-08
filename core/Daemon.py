"""Librairie to manage daemon.
"""
from core import Log
from core import ModuleManager

import sys


__is_running = False


def is_running():
    """Deamon running ?."""
    return __is_running


def start():
    """Start daemon."""
    global __is_running
    Log.init()

    ModuleManager.init_all()
    ModuleManager.start_all()

    __is_running = True

    try:
        ModuleManager.run_loop()
    except KeyboardInterrupt:
        pass

    stop()


def stop():
    """Stop daemon."""
    global __is_running

    if __is_running == False:
        return

    Log.info('stop deamon')
    __is_running = False
    ModuleManager.stop_all()
    sys.exit(0)
