"""Librairie to manage data files.
"""
from core.settings import DATA_PATH

from hashlib import sha256
import hmac
import json
import os


def delete(module_name, file_name):
    """Delete content data."""
    path = get_path(module_name, file_name)

    if os.path.isfile(path):
        os.remove(path)

def get_path(module_name, file_name):
    """Get data file path."""
    h = hmac.new(module_name.encode(), file_name.encode(), sha256).hexdigest()
    return os.path.join(DATA_PATH, h)


def load(module_name, file_name, default_value=None):
    """Get content data."""
    path = get_path(module_name, file_name)

    if not os.path.isfile(path):
        return default_value

    with open(path, 'r') as f:
        return json.load(f)


def save(module_name, file_name, content):
    """Set content data."""
    with open(get_path(module_name, file_name), 'w') as f:
        json.dump(content, f)

# create DATA_PATH directory
if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)
