"""Librairie to manage modules.
"""
from core import DataFileManager, Log
from core.settings import *

from datetime import datetime
import os
import threading


__active_modules_name = []
__modules_data = {}  # module data


def call(module_name, method_name, *arg, _optional_call=False, **kwargs):
    """Call module method."""
    if not module_name in __modules_data:
        if not _optional_call:
            Log.error('Module "%s" not found' % module_name)
        return False

    if __modules_data[module_name]['instance'] is None:
        if not _optional_call:
            Log.error('Module "%s" is not instantiated' % module_name)
        return False

    if not hasattr(__modules_data[module_name]['instance'], method_name):
        if not _optional_call:
            Log.error('Module "%s" has not a "%s" method' % (module_name, method_name))
        return False

    return getattr(__modules_data[module_name]['instance'], method_name)(*arg, **kwargs)


def disable_module(module_name, disabled=True):
    """Disable a module."""
    if module_name in __modules_data:
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
    """Get module instance."""
    # If module is on __modules_data we return its instance
    return __modules_data[module_name]['instance'] if \
        module_name in __modules_data else None


def get_info(module_name, key, default=None):
    """Get module info by key."""
    infos = get_infos(module_name)
    return infos[key] if key in infos else default


def get_infos(module_name):
    """Get module infos."""
    return __modules_data[module_name] if module_name in __modules_data else {}


def get_active_modules():
    """Get active module name list."""
    return __active_modules_name


def get_all_modules():
    """Get all (with disabled) module name list."""
    return __modules_data.keys()


def is_disabled(module_name):
    """Is module disabled."""
    dir_path = os.path.join(MODULES_PATH, module_name)

    # If path is not a directory the module is disabled
    if not os.path.isdir(dir_path):
        return True

    # We check if disabled file exist inside module directory
    return os.path.isfile(os.path.join(dir_path, 'disabled'))


def init(module_name):
    """Init module."""
    if is_disabled(module_name):
        return False

    if module_name in __modules_data and not __modules_data[module_name]['instance']:

        dir_path = os.path.join(MODULES_PATH, module_name)

        module_file = os.path.join(dir_path, 'Module.py')
        if not os.path.isfile(module_file):
            return False

        try:
            module = __import__(
                'modules.' + module_name + '.Module',
                globals(),
                locals(),
                ['Module'],
            ).Module()

            if not module.is_available():
                del(module)
                return False

            module.name = module_name
            module.internal_init()
            __modules_data[module_name]['instance'] = module
            Log.debug('init module %s' % module_name)

        except ImportError as e:
            Log.error(
                'Import error, module %s (%s):' % (module_name, e),
                exc_info=True
            )
            return False

        except AttributeError as e:
            Log.error(
                'Module error, module %s (%s)' % (module_name, e),
                exc_info=True
            )
            return False

    return True


def init_all():
    """Init all modules."""
    __index_modules()
    initialized = [init(module_name) for module_name in __modules_data.copy()]

    Log.info('%d modules initialized' % sum(initialized))


def reindex_modules():
    """Reload all modules in module_list."""
    __index_modules(reload=True)


def restart(module_name):
    """Restart module."""
    Log.info('restart "%s" module' % module_name)
    stop(module_name)
    start(module_name)


def run_loop():
    """Run loop (for update cron)"""
    from . import Daemon  # loop import

    last_timestamp_cron = {
        i: DataFileManager.load('core::ModuleManager', 'cron_%s' % i, 0)
        for i in ['day', 'hour', 'min', 'month', 'week', 'year']
    }

    while Daemon.is_running():
        current_time = time.time()
        current_datetime = datetime.now()

        # cron min
        if 60 <= current_time - last_timestamp_cron['min']:
            last_timestamp_cron['min'] = current_time
            __run_cron('min', current_time)

        # cron hour
        if 60*60 <= current_time - last_timestamp_cron['hour']:
            last_timestamp_cron['hour'] = current_time
            __run_cron('hour', current_time)

        # cron day
        if current_datetime.today() > datetime.fromtimestamp(last_timestamp_cron['day']).today():
            last_timestamp_cron['day'] = current_time
            __run_cron('day', current_time)

        # cron week
        last = datetime.fromtimestamp(last_timestamp_cron['week'])
        if current_datetime.today() != last.today() and current_datetime.weekday() == last.weekday():
            last_timestamp_cron['week'] = current_time
            __run_cron('week', current_time)

        # cron month
        if current_datetime.month != datetime.fromtimestamp(last_timestamp_cron['month']).month:
            last_timestamp_cron['month'] = current_time
            __run_cron('month', current_time)

        # cron year
        if current_datetime.year > datetime.fromtimestamp(last_timestamp_cron['year']).year:
            last_timestamp_cron['year'] = current_time
            __run_cron('year', current_time)

        time.sleep(1)


def start(module_name):
    """Start module."""
    if is_disabled(module_name):
        return False

    if not module_name in __modules_data or __modules_data[module_name]['instance'] is None:
        return False

    __modules_data[module_name]['instance'].started()
    __modules_data[module_name]['instance'].is_running = True
    __modules_data[module_name]['thread'] = threading.Thread(
        None,
        __modules_data[module_name]['instance'].run,
        'module: %s' % module_name
    )
    __modules_data[module_name]['thread'].setDaemon(True)
    __modules_data[module_name]['thread'].start()

    __active_modules_name.append(module_name)

    Log.info('start "%s" module' % module_name)
    return True


def start_all():
    """Start all modules."""
    started = [not __modules_data[module_name]['disabled'] and start(module_name) for module_name in __modules_data]
    Log.info('%d modules started' % sum(started))


def stop(module_name):
    """Stop module."""
    __active_modules_name.remove(module_name)
    Log.info('stop "%s" module' % module_name)

    __modules_data[module_name]['instance'].stopped()
    __modules_data[module_name]['instance'].is_running = False
    __modules_data.pop(module_name)

    return True


def stop_all():
    """Stop all modules."""
    nb = 0

    for module_name in __modules_data.copy():
        if __modules_data[module_name]['instance'] and stop(module_name):
            nb += 1

    Log.info('%d modules stopped' % nb)


def __index_modules(reload=False):
    """Add all modules in module_list."""
    global __modules_data

    if __modules_data and not reload:
        return

    dir_list = sorted(os.listdir(MODULES_PATH))
    nb = 0

    __modules_data.clear()
    for module_name in dir_list:

        if is_disabled(module_name):
            continue

        if '__pycache__' in module_name:
            continue

        __modules_data[module_name] = {
            'disabled': False,
            'instance': None,
            'thread': None
        }
        Log.debug('index "%s" module' % module_name)
        nb += 1

    Log.info('%d modules indexed' % nb)


def __run_cron(cron_type, current_time):
    cron_type = 'cron_%s' % cron_type
    DataFileManager.save('core::ModuleManager', cron_type, current_time)

    for module_name in __modules_data:
        if not __modules_data[module_name]['instance']:
            continue

        handler = getattr(__modules_data[module_name]['instance'], cron_type)

        # handler has implemented ?
        if len(handler.__code__.co_code) > 4:
            threading.Thread(None, handler, '%s: %s' % (cron_type, module_name)).start()
