"""Librairie to manage circuits.
"""
from core import Log
from core.settings import NAME, ROOT_PATH

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
        register(daemon.Daemon(
            '%s.pid' % NAME,
            path=ROOT_PATH
        ))

    Worker().register(__manager)
    __manager.run()


def stop():
    __manager.stop()

