"""Librairie to manage circuits.
"""
from core import Log

from circuits import Manager, Worker


__manager = Manager()


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
