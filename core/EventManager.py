"""Librairie to manage events.
"""

from core import Log

__event_handle_list = {}


def bind(event_name):
    """Decorator for function.
    """
    def decorator(handle):
        bind_handle(event_name, handle)
        return handle
    return decorator


def bind_handle(event_name, handle):
    """Attach a handler to an event.
    """
    if not event_name in __event_handle_list:
        __event_handle_list[event_name] = []

    __event_handle_list[event_name].append(handle)
    Log.debug('bin event : "%s" to "%s"' % (event_name, str(handle)))


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

