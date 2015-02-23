import os
import time

NAME = 'MoLA'
START_TIME = time.time()
ROOT_PATH = os.sep.join(__file__.split(os.sep)[:-2])
CONFIGS_PATH = os.path.join(ROOT_PATH, 'configs')
MODULES_PATH = os.path.join(ROOT_PATH, 'modules')

