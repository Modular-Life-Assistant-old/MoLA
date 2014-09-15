"""Librairie to manage modules.
"""

from core import CircuitsManager
from core import Log

import os

__module_list = {}  # module data


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


def disable_module(module_name, disabled=True):
    """Disable a module.
    """
    if module_name in __module_list:
        return False

    from core import Daemon

    path = '%s%s/disable' % (Daemon.MODULES_PATH, module_name)

    if disabled:
        stop(module_name)

        with open(path, 'a'):
            os.utime(path, None)

        return True

    else:
        if os.path.isfile(path):
            os.remove(path)

        start(module_name)


def get(module_name):
    """Get module instance.
    """
    return __module_list[module_name]['instance'] if module_name in __module_list else None


def is_module_disabled(module_name):
    """Is module disable.
    """
    from core import Daemon

    dir_path = '%s%s/' % (Daemon.MODULES_PATH, module_name)
    if not os.path.isdir(dir_path):
        return True

    return os.path.isfile('%s/disable' % dir_path)


def init(module_name):
    """Init module.
    """
    if is_module_disabled(module_name):
        return False

    if module_name in __module_list and not __module_list[module_name]['instance']:
        from core import Daemon

        dir_path = '%s%s/' % (Daemon.MODULES_PATH, module_name)

        module_path = '%sModule.py' % dir_path
        if not os.path.isfile(module_path):
            return False

        try:
            __module_list[module_name]['instance'] = __import__(
                'modules.' + module_name + '.Module',
                globals(),
                locals(),
                ['Module'],
            ).Module()

        except ImportError as e:
            Log.error('Import error, module %s (%s)' % (module_name, e))
            return False

    return True


def init_all():
    """Init all modules.
    """
    __load_module_list()
    loaded = [init(module_name) for module_name in __module_list]

    Log.debug('%d modules initialized' % sum(loaded))


def load(module_name):
    """Load module.
    """
    if is_module_disabled(module_name):
        return False

    if module_name in __module_list and __module_list[module_name]['instance'] is not None:
        call_module_method(module_name, 'load_configuration')
        return True

    return False


def load_all():
    """Load all modules.
    """
    __load_module_list()
    loaded = [load(module_name) for module_name in __module_list]

    Log.debug('%d modules loaded' % sum(loaded))


def restart(module_name):
    """Restart module.
    """
    Log.debug('restart modules %s' % module_name)
    stop(module_name)
    start(module_name)


def start(module_name):
    """Start module.
    """
    if is_module_disabled(module_name):
        return False

    if not module_name in __module_list or __module_list[module_name]['instance'] is None:
        return False

    CircuitsManager.register(__module_list[module_name]['instance'])
    return True


def start_all():
    """Start all modules.
    """
    __load_module_list()
    started = [not __module_list[module_name]['disable'] and start(module_name) for module_name in __module_list]
    Log.debug('%d modules started' % sum(started))


def stop(module_name):
    """Stop module.
    """
    Log.debug('stop modules %s' % module_name)
    call_module_method(module_name, 'stop')
    return True


def stop_all():
    """Stop all modules.
    """
    nb = 0

    for module_name in __module_list:
        if __module_list[module_name]['instance'] and stop(module_name):
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

    for module_name in dir_list:
        dir_path = '%s%s/' % (Daemon.MODULES_PATH, module_name)

        if is_module_disabled(module_name):
            continue

        if '__pycache__' in module_name:
            continue

        __module_list[module_name] = {
            'instance': None,
            'disable': False,
        }
        nb += 1

    Log.debug('%d modules indexed' % nb)

