import os
import re
import sys
import time

NAME = 'MoLA'
START_TIME = time.time()
ROOT_PATH = os.sep.join(__file__.split(os.sep)[:-2])
CONFIGS_PATH = os.path.join(ROOT_PATH, 'configs')
DATA_PATH = os.path.join(ROOT_PATH, 'data')
MODULES_PATH = os.path.join(ROOT_PATH, 'modules')

for arg in sys.argv:
    if '--name=' in arg:
        NAME = re.sub('[^0-9a-zA-Z]+', '-', arg.split('--name=')[1])
        break