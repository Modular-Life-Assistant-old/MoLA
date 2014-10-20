import json
import logging
import logging.config
import os


__logger = None
LOGS_PATH = ''


def init():
    from core import Daemon
    global __logger
    global LOGS_PATH
    
    LOGS_PATH = os.path.join(Daemon.ROOT_PATH, 'logs')
    LOG_CONF = os.path.join(Daemon.CONFIGS_PATH, 'log.conf')
    log_list = []

    with open(LOG_CONF) as config_file:
        config = json.load(config_file)

        # place in log directory
        if 'handlers' in config:
            if not os.path.exists(LOGS_PATH):
                os.makedirs(LOGS_PATH)

            for handler in config['handlers']:
                if 'filename' in config['handlers'][handler] and config['handlers'][handler]['filename']:
                    config['handlers'][handler]['filename'] = os.path.join(
                        LOGS_PATH,
                        config['handlers'][handler]['filename']
                    )
                    log_list.append(config['handlers'][handler])

        logging.config.dictConfig(config)
    __logger = logging.getLogger(Daemon.name)

    for log in log_list:
        info('Log %s in %s' % (
            log['level'] if 'level' in log else 'Unknow level', 
            log['filename']
        ))


def crash(text):
    __logger.critical(text, exc_info=True)


def critical(text, tag=[]): # score: 50
    __logger.critical(text, extra={'tags':tag})


def debug(text, tag=[]): # score: 10
    __logger.debug(text, extra={'tags':tag})


def error(text, tag=[]): # score: 40
    __logger.error(text, extra={'tags':tag})


def get_logger():
    return __logger


def has_debug():
    return __logger.isEnabledFor(logging.DEBUG)


def info(text, tag=[]): # score: 20
    __logger.info(text, extra={'tags':tag})


def warning(text, tag=[]):# score: 30
    __logger.warn(text, extra={'tags':tag})