import json
import logging
import logging.config
import os
import sys

from core.settings import ROOT_PATH, CONFIGS_PATH, NAME

__logger = logging.getLogger(NAME)
LOGS_PATH = ''


def init():
    global LOGS_PATH
    
    LOGS_PATH = os.path.join(ROOT_PATH, 'logs')
    LOG_CONF = os.path.join(CONFIGS_PATH, 'log.json')
    log_list = []

    with open(LOG_CONF) as config_file:
        config = json.load(config_file)

        # place in log directory
        if 'handlers' in config:
            if not os.path.exists(LOGS_PATH):
                os.makedirs(LOGS_PATH)

            for handler in config['handlers']:
                if 'filename' in config['handlers'][handler] and \
                        config['handlers'][handler]['filename']:
                    config['handlers'][handler]['filename'] = os.path.join(
                        LOGS_PATH, '%s-%s' % (
                            NAME, config['handlers'][handler]['filename']
                        )
                    )
                    log_list.append(config['handlers'][handler])

        logging.config.dictConfig(config)

    for log in log_list:
        info('Log %s in %s' % (
            log['level'] if 'level' in log else 'Unknow level', 
            log['filename']
        ))

    # rewrite currentframe function  (for receive correct file / line number)
    if hasattr(sys, '_getframe'):
        currentframe = lambda: sys._getframe(4)
    else: #pragma: no cover
        def currentframe():
            """Return the frame object for the caller's stack frame."""
            try:
                raise Exception
            except Exception:
                return sys.exc_info()[3].tb_frame.f_back

    logging.currentframe = currentframe


def crash(text, *args, **kwargs):
    kwargs['exc_info'] = True
    __logger.critical(text, *args, **kwargs)


def critical(text, *args, **kwargs): # score: 50
    __logger.critical(text, *args, **kwargs)


def debug(text, *args, **kwargs): # score: 10
    __logger.debug(text, *args, **kwargs)


def error(text, *args, **kwargs): # score: 40
    __logger.error(text, *args, **kwargs)


def get_logger():
    return __logger


def has_debug():
    return __logger.isEnabledFor(logging.DEBUG)


def info(text, *args, **kwargs): # score: 20
    __logger.info(text, *args, **kwargs)


def warning(text, *args, **kwargs):# score: 30
    __logger.warn(text, *args, **kwargs)
