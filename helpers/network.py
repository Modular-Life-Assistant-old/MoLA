import os
import subprocess
from core import Log


def get_arp_infos():
    """Get arp infos.

    :return: arp infos dict
    """

    if os.name == 'nt':
        return _get_arp_infos_windows()

    return _get_arp_infos_linux()


def _get_arp_infos_linux():
    """Get arp infos.

    :return: arp infos dict
    """
    result = {}

    # ping sweep
    try:
        subprocess.check_output('ping 255.255.255.255 -b -c 1', shell=True)
    except subprocess.CalledProcessError as e:
        Log.error('Network helper: ping sweep: %s' % e)

    output = subprocess.check_output('arp -e', shell=True)
    if not output:
        return result

    for line in output.split(b'\n'):
        if not line or b'gateway' in line or b'incomplete' in line:
            continue

        data = line.split()
        result[data[0].decode()] = {
            'mac': data[2].decode().replace(':', ''),
            'is_dynamic': True,  # entry are remove on inactive
        }

    return result


def _get_arp_infos_windows():
    """Get arp infos.

    :return: arp infos dict
    """
    result = {}

    output = subprocess.check_output('arp -a', shell=True)
    if not output:
        return result

    for line in output.split(b'\n'):
        if not line or len(line.split()) != 3:
            continue

        ip, mac, type = line.split()
        result[ip.decode()] = {
            'mac': mac.decode().replace('-', ''),
            'is_dynamic': b'ynami' in type,  # entry are remove on inactive
        }

    return result