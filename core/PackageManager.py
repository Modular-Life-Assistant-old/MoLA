import json
import os
import shutil
import requests
from io import BytesIO
from zipfile import ZipFile

from core import Log, ModuleManager
from core.settings import CONFIGS_PATH, MODULES_PATH


def get_config():
    """Get config content

    :return: config dict
    """
    with open(os.path.join(CONFIGS_PATH, 'repository.json')) as f:
        return json.load(f)


def get_module_infos(module_name):
    """Get module informations.

    :param module_name: module name
    :return: dict infos
    """
    return _get_infos('module', module_name)


def get_project_infos(project_name):
    """Get project informations.

    :param project_name: project name
    :return: dict infos
    """
    return _get_infos('project', project_name)


def install_module(module_name):
    """Install a new module.

    :param module_name: module name
    :return: is sucess
    """
    module_path = os.path.join(MODULES_PATH, module_name)
    if os.path.exists(module_path):
        return False

    infos = get_module_infos(module_name)
    if not infos:
        Log.error('Module "%s" not found' % module_name)
        return False

    # install module
    zip_file = BytesIO(requests.get(infos['zip_url']).content)
    with ZipFile(zip_file) as z:
        # security + locate path files
        content_dir = ''
        for member in z.namelist():
            if member.startswith('/') or './' in member:
                Log.critical('Security threat on "%s" module install (%s)' % (
                             module_name, member))
                return False

            if 'Module.py' in member:
                content_dir = member.replace('Module.py', '')

        # unzip
        os.makedirs(module_path)
        for member in z.namelist():
            # skip directories
            if not os.path.basename(member):
                continue

            # unzip
            path = os.path.join(module_path, member.replace(content_dir, ''))
            with z.open(member) as s, open(path, 'wb') as t:
                shutil.copyfileobj(s, t)

    # starting module
    ModuleManager.reindex_modules()
    ModuleManager.init(module_name)
    ModuleManager.start(module_name)
    return True


def update_module(module_name):
    """Update a module.

    :param module_name: module name
    :return: is sucess
    """
    if not ModuleManager.get(module_name):
        Log.error('Module not installed')
        return False


def _get_infos(item_type, item_name):
    """Get item informations.

    :param item_type: item type (module, project, ...)
    :param module_name: item name
    :return: dict infos
    """
    for url in get_config().get('%s_info' % item_type, []):
        r = requests.get(url + item_name + '.json')
        if r:
            return r.json()

    return {}
