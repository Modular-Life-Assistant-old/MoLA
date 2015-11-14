"""Librairie to manage notifications.
"""
from core import Log

import threading


__notify_handlers = {}


def notify(source, msg, image=None, sound=None):
    """ send a notification."""
    Log.info('notify: %s / %s / %s' % (msg, image, sound))
    for handler in __notify_handlers.values():
        threading.Thread(
            target=handler, name='Notification: %s' % str(handler),
            kwargs={'msg': msg, 'image': image, 'sound': sound}
        ).start()


def register(module_name, handler):
    """Register a handler."""
    __notify_handlers[module_name] = handler
