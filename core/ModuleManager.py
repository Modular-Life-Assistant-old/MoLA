"""Librairie to manage modules.
"""

from core import Log

import os

__module_list = {} # module data


def call_module_method(module_name, method_name, *arg):
    """Call module method.
    """
    if not module_name in __module_list:
        return False

    if not __module_list[module_name]['instance']:
        return False

    if not hasattr(__module_list[module_name]['instance'], method_name):
        return False

    return getattr(__module_list[module_name]['instance'], method_name)(*arg)


def get(name):
    """Get module instance.
    """
    return __module_list[name]['instance'] if name in __module_list else None


def load(name):
    """load module.
    """
    from core import Daemon
    dir_path = '%s%s/' % (Daemon.MODULES_PATH, name)
    if not os.path.isdir(dir_path):
        return False

    if name in __module_list and not __module_list[name]['instance']:
        module_path = '%sModule.py' % dir_path
        if os.path.isfile(module_path):
            return False

        try:
            __module_list[name]['instance'] = __import__(
                'modules.' + name + '.Module',
                globals(),
                locals(),
                ['Module'],
                -1
            ).Module()

        except ImportError as e:
            Log.error('Import error, module %s (%s)' % (name, e))
            return False

    call_module_method(name, 'load_configuration')

    return True


def load_all():
    """Start all modules.
    """
    __load_module_list()
    nb = 0

    for name in __module_list:
        if not __module_list[name]['disable']:
            load(name)
            nb += 1

    Log.debug('%d modules loaded' % nb)


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

    Log.debug('%d modules indexed' % nb)
