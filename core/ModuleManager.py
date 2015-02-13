"""Librairie to manage modules.
"""

from core import CircuitsManager
from core import Log
from core.settings import *

import os

__modules_list = {}  # module data


def call_module_method(module_name, method_name, *arg, **kwargs):
    """Call module method.
    """
    if not module_name in __modules_list:
        Log.error('Module "%s" not found' % module_name)
        return False

    if __modules_list[module_name]['instance'] is None:
        Log.error('Module "%s" is not instantiated' % module_name)
        return False

    if not hasattr(__modules_list[module_name]['instance'], method_name):
        Log.error('Module "%s" has not a "%s" method' % (module_name, method_name))
        return False

    return getattr(__modules_list[module_name]['instance'], method_name)(*arg, **kwargs)


def disable_module(module_name, disabled=True):
    """Disable a module.
    """
    if module_name in __modules_list:
        return False

    disable_file = os.path.join(MODULES_PATH, module_name, 'disabled')

    if disabled:
        stop(module_name)

        with open(disable_file, 'a'):
            os.utime(disable_file, None)

        return True

    else:
        if os.path.isfile(disable_file):
            os.remove(disable_file)

        start(module_name)


def get(module_name):
    """Get module instance.
    """
    # If module is on __modules_list we return its instance
    return __modules_list[module_name]['instance'] if \
        module_name in __modules_list else None


def is_disabled(module_name):
    """Is module disabled.
    """
    dir_path = os.path.join(MODULES_PATH, module_name)

    # If path is not a directory the module is disabled
    if not os.path.isdir(dir_path):
        return True

    # We check if disabled file exist inside module directory
    return os.path.isfile(os.path.join(dir_path, 'disabled'))


def init(module_name):
    """Init module.
    """
    if is_disabled(module_name):
        return False

    if module_name in __modules_list and not __modules_list[module_name]['instance']:

        dir_path = os.path.join(MODULES_PATH, module_name)

        module_file = os.path.join(dir_path, 'Module.py')
        if not os.path.isfile(module_file):
            return False

        try:
            __modules_list[module_name]['instance'] = __import__(
                'modules.' + module_name + '.Module',
                globals(),
                locals(),
                ['Module'],
            ).Module()
            Log.debug('init module %s' % module_name)

        except ImportError as e:
            Log.error('Import error, module %s (%s)' % (module_name, e))
            return False

        except AttributeError as e:
            Log.error('Module error, module %s (%s)' % (module_name, e))
            return False

    return True


def init_all():
    """Init all modules.
    """
    __index_modules()
    initialized = [init(module_name) for module_name in __modules_list]

    Log.info('%d modules initialized' % sum(initialized))


def reindex_modules():
    __index_modules(reload=True)


def restart(module_name):
    """Restart module.
    """
    Log.info('restart "%s" module' % module_name)
    stop(module_name)
    start(module_name)


def start(module_name):
    """Start module.
    """
    if is_disabled(module_name):
        return False

    if not module_name in __modules_list or __modules_list[module_name]['instance'] is None:
        return False

    # is Circuits module ?
    if hasattr(__modules_list[module_name]['instance'], 'register'):
        CircuitsManager.register(__modules_list[module_name]['instance'])
    elif hasattr(__modules_list[module_name]['instance'], 'started'):
        __modules_list[module_name]['instance'].started()

    Log.info('start "%s" module' % module_name)
    return True


def start_all():
    """Start all modules.
    """
    started = [not __modules_list[module_name]['disabled'] and start(module_name) for module_name in __modules_list]
    Log.info('%d modules started' % sum(started))


def stop(module_name):
    """Stop module.
    """
    Log.info('stop "%s" module' % module_name)

    if hasattr(__modules_list[module_name]['instance'], 'unregister'):
        CircuitsManager.unregister(__modules_list[module_name]['instance'])
    elif hasattr(__modules_list[module_name]['instance'], 'stopped'):
        __modules_list[module_name]['instance'].stopped()

    __modules_list.pop(module_name)

    return True


def stop_all():
    """Stop all modules.
    """
    nb = 0

    for module_name in __modules_list:
        if __modules_list[module_name]['instance'] and stop(module_name):
            nb += 1

    Log.info('%d modules stopped' % nb)


def __index_modules(reload=False):
    """Add all modules in module_list.
    """
    global __modules_list

    if __modules_list and not reload:
        return

    dir_list = sorted(os.listdir(MODULES_PATH))
    nb = 0

    __modules_list.clear()
    for module_name in dir_list:

        if is_disabled(module_name):
            continue

        if '__pycache__' in module_name:
            continue

        __modules_list[module_name] = {
            'instance': None,
            'disabled': False,
        }
        Log.debug('index "%s" module' % module_name)
        nb += 1

    Log.info('%d modules indexed' % nb)
