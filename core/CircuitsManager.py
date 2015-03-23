"""Librairie to manage circuits.
"""
from core import Log
from core import ModuleManager

from circuits import Component, Event, Manager, Worker


__manager = Manager()


def call_lib(module_name, method_name, *arg, **kwargs):
    """Call lib.
    """
    instance = module_name if isinstance(module_name, Component) else \
        ModuleManager.get(module_name)

    if isinstance(instance, Component) is None:
        Log.error('Module "%s" not found' % module_name)
        return False

    if not hasattr(instance, method_name):
        Log.error('Module "%s" has not a "%s" method' % (
            module_name, method_name
        ))
        return False

    event = Event.create(method_name, *arg, **kwargs)
    return instance.call(event, instance.channel)


def register(instance):
    instance.register(__manager)


def run_loop():
    if Log.has_debug():
        from circuits import Debugger
        register(Debugger(logger=Log.get_logger()))

    Worker().register(__manager)
    __manager.run()


def stop():
    __manager.stop()
