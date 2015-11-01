"""Librairie to manage notifications.
"""
from core import Log

import threading


__event_handlers = {}


class Event:
    args = ()
    name = ''
    kwargs = {}

    def __init__(self, name, *args, **kwargs):
        self.args = args
        self.name = name
        self.kwargs = kwargs


def fire(source, event):
    """ send a event."""
    Log.debug('event: %s' % event)

    if event.name not in __event_handlers:
       return

    for handler in __event_handlers[event.name]:
        threading.Thread(None, handler, 'Event: %s at %s' % (event, str(handler)), (event,)).start()


def register(event_name, handler):
    """Register a handler."""
    Log.debug('register handler event: %s for %s' % (handler, event_name))

    if event_name not in __event_handlers:
        __event_handlers[event_name] = []

    __event_handlers[event_name].append(handler)
