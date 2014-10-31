"""Librairie to manage daemon.
"""

from core import CircuitsManager
from core import Log
from core import ModuleManager

import os
import time

name = 'MoLA'
START_TIME = time.time()
ROOT_PATH = os.sep.join(__file__.split(os.sep)[:-2])
CONFIGS_PATH = os.path.join(ROOT_PATH, 'configs')
MODULES_PATH = os.path.join(ROOT_PATH, 'modules')


def launch_daemon():
    """start new application.
    """
    daemon_path = os.path.join(ROOT_PATH, 'daemon.py')
    return os.system('"%s" 1> /dev/null 2>&1 &' % daemon_path) == 0


def restart():
    """Restart daemon.
    """
    stop()
    launch_daemon()


def start():
    """Start daemon.
    """
    Log.init()
    ModuleManager.init_all()
    ModuleManager.load_all()
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
