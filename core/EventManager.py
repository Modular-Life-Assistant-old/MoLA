"""Librairie to manage notifications.
"""
from core import Log

import threading


__event_handlers = {}


class Event:
    def __init__(self, name, source, parent=None, *args, **kwargs):
        """Init a new event

        :param name: event name
        :param source: event source object (instance of module, device, ...)
        :param parent: event parent (event object)
        :param args: event args
        :param kwargs: event kwargs
        """
        self.args = args
        self.kwargs = kwargs
        self.name = name
        self.parent = parent
        self.source = source


def fire(event):
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
