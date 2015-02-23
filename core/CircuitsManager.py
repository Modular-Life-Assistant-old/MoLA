"""Librairie to manage circuits.
"""
from core import Log

from circuits.app import daemon
from circuits import Manager, Worker
import sys

__manager = Manager()


def register(instance):
    instance.register(__manager)


def run_loop():
    if Log.has_debug():
        from circuits import Debugger
        register(Debugger(logger=Log.get_logger()))

    if not '--no-daemon' in sys.argv:
        from core import Daemon
        register(daemon.Daemon(
            '%s.pid' % Daemon.name,
            path=Daemon.ROOT_PATH
        ))

    Worker().register(__manager)
    __manager.run()


def stop():
    __manager.stop()

