"""Librairie to manage daemon.
"""
from core import Log
from core import ModuleManager
from core import settings

import sys


__is_running = False


def is_running():
    """Deamon running ?."""
    return __is_running


def start():
    """Start daemon."""
    global __is_running
    settings.load_conf()
    Log.init()

    ModuleManager.init_all()
    ModuleManager.load_config_all()
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

    if not __is_running:
        return

    Log.info('stop deamon')
    __is_running = False
    ModuleManager.stop_all()
    sys.exit(0)
