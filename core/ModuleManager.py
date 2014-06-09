"""Librairie to manage modules.
"""

from core import Log

import os

__module_list = {} # module data


def get(name):
    """Get module instance.
    """
    return __module_list[name]['instance'] if name in __module_list else None


def restart(name):
    """Restart module.
    """
    Log.debug('restart modules %s' % name)
    stop(name)
    start(name)


def start(name):
    """Start module.
    """
    # todo
    return True


def start_all():
    """Start all modules.
    """
    __load_module_list()
    nb = 0

    for name in __module_list:
        if not __module_list[name]['disable']:
            start(name)
            nb += 1

    Log.debug('%d modules started' % nb)


def stop(name):
    """Stop module.
    """
    Log.debug('stop modules %s' % name)
    # todo


def stop_all():
    """Stop all modules.
    """
    nb = 0

    for name in __module_list:
        if __module_list[name]['instance']:
            stop(name)
            nb += 1

    Log.debug('%d modules stoped' % nb)


def __load_module_list():
    """Add all modules in module_list.
    """
    global __module_list

    if __module_list:
        return

    from core import Daemon

    dir_list = sorted(os.listdir(Daemon.MODULES_PATH))
    nb = 0

    for name in dir_list:
        if os.path.isdir('%s%s' % (Daemon.MODULES_PATH, name)):
            __module_list[name] = {
                'instance': None,
                'disable':  False,
            }
            nb += 1

    Log.debug('%d modules loaded' % nb)
