"""Librairie to manage notifications.
"""
from core import Log

import threading


__notify_handlers = {}


def notify(source, msg):
    """ send a notification
    """
    Log.info('notify: %s' % msg)
    for handler in __notify_handlers.values():
        threading.Thread(None, handler, 'Notification: %s' % str(handler), (msg,)).start()


def register(module_name, handler):
    __notify_handlers[module_name] = handler
