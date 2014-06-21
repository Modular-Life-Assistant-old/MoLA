"""Librairie to manage modules.
"""

from core import Log

import os

__module_list = {} # module data
__action_method_list = []

def add_method_action(method_name, handle_start=None, handle_stop=None):
    """Add a method action.
    """
    __action_method_list.append({
        'method_name':  method_name,
        'handle_start': handle_start,
        'handle_stop':  handle_stop,
    })


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
    nb = 0

    for module_name in __module_list:
        if not __module_list[module_name]['disable'] and init(module_name):
            nb += 1

    Log.debug('%d modules initialized' % nb)


def load(module_name):
    """Load module.
    """
    if is_module_disabled(module_name):
        return False

    if module_name in __module_list and __module_list[module_name]['instance']:
        call_module_method(module_name, 'load_configuration')
        return True

    return False


def load_all():
    """Load all modules.
    """
    __load_module_list()
    nb = 0

    for module_name in __module_list:
        if not __module_list[module_name]['disable'] and load(module_name):
            nb += 1

    Log.debug('%d modules loaded' % nb)


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

    if not module_name in __module_list or not __module_list[module_name]['instance']:
        return False

    __call_method_action(module_name, 'handle_start')

    return True


def start_all():
    """Start all modules.
    """
    __load_module_list()
    nb = 0

    for module_name in __module_list:
        if not __module_list[module_name]['disable'] and start(module_name):
            nb += 1

    Log.debug('%d modules started' % nb)


def stop(module_name):
    """Stop module.
    """
    Log.debug('stop modules %s' % module_name)

    __call_method_action(module_name, 'handle_stop')

    return True


def stop_all():
    """Stop all modules.
    """
    nb = 0

    for module_name in __module_list:
        if __module_list[module_name]['instance'] and stop(module_name):
            nb += 1

    Log.debug('%d modules stoped' % nb)


def __call_method_action(module_name, handle_name):
    """Call a method action.
    """
    if not module_name in __module_list:
        return False

    if not __module_list[module_name]['instance']:
        return False

    if not handle_name in ['handle_start', 'handle_stop']:
        return False

    instance = __module_list[module_name]['instance']

    for method_name in dir(instance):
        for action_method in __action_method_list:
            if method_name.startswith(action_method['method_name']):
                action_method[handle_name](
                    module_name,
                    getattr(instance, method_name)
                )


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
            'disable':  False,
        }
        nb += 1

    Log.debug('%d modules indexed' % nb)
