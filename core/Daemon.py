"""Librairie to manage daemon.
"""

from core import CircuitsManager
from core import Log
from core import ModuleManager

import os
import time

name = 'MoLA'
start_time = time.time()
ROOT_PATH = '%s/' % os.sep.join(__file__.split(os.sep)[:-2])
CONFIGS_PATH = '%sconfigs/' % ROOT_PATH
MODULES_PATH = '%smodules/' % ROOT_PATH

def launch_daemon():
    """start new application.
    """
    return os.system('"%sdaemon.py" 1> /dev/null 2>&1 &' % ROOT_PATH) == 0


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

    except KeyboardInterrupt:
        Log.info('Exit : KeyboardInterrupt')

    except Exception as e:
        Log.crash(e)

    finally:
        stop()


def stop():
    """Stop daemon.
    """
    Log.info('stop deamon')
    ModuleManager.stop_all()
