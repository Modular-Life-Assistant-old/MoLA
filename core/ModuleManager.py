"""Librairie to manage modules.
"""

from core import Log

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
    # todo
    pass


def stop(name):
    """Stop module.
    """
    Log.debug('stop modules %s' % name)
    # todo


def stop_all():
    """Stop all modules.
    """
    # todo
    pass


def __load_module_list():
    """Add all modules in module_list.
    """
    modules_list = sorted(os.listdir(Variables.root_path + 'modules'))
    nb = 0

    for name in modules_list:
        __module_list[name] = {
            'instance': None,
        }
        nb += 1

    Log.debug('%d modules loaded' % nb)
