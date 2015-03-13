"""Librairie to manage daemon.
"""
from core import CircuitsManager
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
        CircuitsManager.run_loop()
    except Exception as e:
        Log.crash(e)
    finally:
        stop()


def stop():
    """Stop daemon.
    """
    Log.info('stop deamon')
    ModuleManager.stop_all()
    CircuitsManager.stop()
    sys.exit(0)
