import json
import logging


__logger = None


def init():
    from core import Daemon
    global __logger

    __logger = logging.getLogger(Daemon.name)
    log_path = '%s%s.log' % (Daemon.ROOT_PATH, Daemon.name)

    hdlr = logging.FileHandler(log_path)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)

    __logger.addHandler(hdlr) 
    __logger.setLevel(logging.DEBUG)
    debug('Log in %s' % log_path)


def crash(text):
    __logger.critical(text, exc_info=True)
    print('Crash: %s' % text)


def critical(text, tag=[]): # score: 50
    __logger.critical(__set_tag(text, tag))
    print('Critical: %s' % text)


def debug(text, tag=[]): # score: 10
    __logger.debug(__set_tag(text, tag))
    print('Debug: %s' % text)


def error(text, tag=[]): # score: 40
    __logger.error(__set_tag(text, tag))
    print('Error: %s' % text)


def info(text, tag=[]): # score: 20
    __logger.info(__set_tag(text, tag))
    print('Info: %s' % text)


def warning(text, tag=[]):# score: 30
    __logger.warn(__set_tag(text, tag))
    print('Warning: %s' % text)


def __set_tag(text, tag):
    if tag:
        text += ' tag:' + json.dumps(tag)
    return text
