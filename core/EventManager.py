"""Librairie to manage events.
"""

from core import Log
from core import ModuleManager

__event_handle_list = {}

def bind_auto():
    """Automatic event binding.
    """
    def start_module(module_name, handle):
        print(module_name)
        event_name = handle.__name__.replace('event_', '')
        bind_handle(event_name, handle)

    ModuleManager.add_method_action(
        'event',
        handle_start=start_module,
    )


def bind_handle(event_name, handle):
    """Attach a handler to an event.
    """
    if not event_name in __event_handle_list:
        __event_handle_list[event_name] = []

    __event_handle_list[event_name].append(handle)
    Log.debug('bind event : "%s" to "%s"' % (event_name, str(handle)))


def trigger(event_name, **data):
    """Execute all handlers attached to the event.
    """
    if not event_name in __event_handle_list:
        Log.debug('no "%s" handle event' % event_name)
        return False

    nb = 0

    for handle in __event_handle_list[event_name]:
        try:
            handle(data)
            nb += 1

        except Exception as e:
            Log.crash(e)

    Log.debug('trigger %d "%s" event' % (nb, event_name))

