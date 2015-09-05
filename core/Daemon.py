"""Librairie to manage daemon.
"""
from core import Log
from core import ModuleManager

import sys


def start():
    """Start daemon.
    """
    Log.init()

    ModuleManager.init_all()
    ModuleManager.start_all()

    try:
        ModuleManager.run_loop()
    except KeyboardInterrupt:
        pass

    stop()


def stop():
    """Stop daemon.
    """
    Log.info('stop deamon')
    ModuleManager.stop_all()
    sys.exit(0)
