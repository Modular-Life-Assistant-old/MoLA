import json
import os
import random
import re
import string
import sys
import time


NAME = 'MoLA'
START_TIME = time.time()
ROOT_PATH = os.sep.join(__file__.split(os.sep)[:-2])
CONFIGS_PATH = os.path.join(ROOT_PATH, 'configs')
DATA_PATH = os.path.join(ROOT_PATH, 'data')
MODULES_PATH = os.path.join(ROOT_PATH, 'modules')
SECRET_KEY = ''


def load_conf():
    config = {}
    config_path = os.path.join(CONFIGS_PATH, 'settings.json')

    # read
    if os.path.isfile(config_path):
        with open(config_path) as f:
            config = json.load(f)

    # set on constant
    for index, value in config.items():
        index = index.upper()
        if index in ('NAME', 'CONFIGS_PATH', 'DATA_PATH',
                     'MODULES_PATH', 'SECRET_KEY'):
            setattr(sys.modules[__name__], index.upper(), value)

    # init value
    global SECRET_KEY
    if not SECRET_KEY:
        SECRET_KEY = "".join([random.SystemRandom().choice(
            string.digits + string.ascii_letters + string.punctuation
        ) for _ in range(100)])
        config['SECRET_KEY'] = SECRET_KEY

    # save
    with open(config_path, 'w+') as f:
        json.dump(config, f)

    # get valur in argument
    for arg in sys.argv:
        if '--name=' in arg:
            global NAME
            NAME = re.sub('[^0-9a-zA-Z]+', '-', arg.split('--name=')[1])
            break