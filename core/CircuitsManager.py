"""Librairie to manage circuits.
"""
from circuits.core.manager import CallValue
from core import Log
from core import ModuleManager

from circuits import Component, Event, handler, Manager, reprhandler, Worker


__manager = Manager()


def call_lib(module_name, method_name, *arg, call_lib_priority=0, **kwargs):
    """Call lib.
    """
    instance = module_name if isinstance(module_name, Component) else \
        ModuleManager.get(module_name)

    if isinstance(instance, Component) is None:
        Log.error('Module "%s" not found' % module_name)
        return CallValue(False)

    if not hasattr(instance, method_name):
        Log.error('Module "%s" has not a "%s" method' % (
            module_name, method_name
        ))
        return CallValue(False)

    event = Event.create(method_name, *arg, **kwargs)
    return instance.call(event, instance.channel, priority=call_lib_priority)


def get_events_queue_size():
    """Returns the number of events in the Event Queue."""
    return len(__manager)


@handler('exception', channel='*', priority=100.0)
def on_exception(self, error_type, value, traceback, handler=None, fevent=None):
    # based on _on_exception (circuits/core/debugger.py line 67)

    s = []
    handler = reprhandler(handler) if handler else ''
    msg = 'ERROR %s (%s) (%s): %s' % (
        handler, repr(fevent), repr(error_type), repr(value)
    )

    s.append(msg)
    s.extend(traceback)
    s.append('\n')

    Log.critical(''.join(s))


def register(instance):
    instance.register(__manager)


def run_loop():
    if Log.has_debug():
        from circuits import Debugger
        register(Debugger(logger=Log.get_logger()))

    else:
        __manager.addHandler(on_exception)

    Worker().register(__manager)
    __manager.run()


def stop():
    __manager.stop()
