"""Librairie to manage circuits.
"""

from core import Log

from circuits import Manager

__manager = Manager()


def register(instance):
    instance.register(__manager)


def run_loop():
    if Log.has_debug():
        from circuits import Debugger
        Debugger(logger=Log.get_logger()).register(__manager)

    __manager.run()
