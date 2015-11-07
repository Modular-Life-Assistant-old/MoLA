import socket
from struct import pack
import subprocess


def get_arp_infos():
    """Get arp infos.

    :return: arp infos dict
    """
    result = {}

    output = subprocess.check_output('arp -a', shell=True)
    if not output:
        return output

    for line in output.split(b'\n'):
        if not line or len(line.split()) != 3:
            continue

        ip, mac, type = line.split()
        result[ip.decode()] = {
            'mac': mac.decode().replace('-', ''),
            'is_dynamic': b'ynami' in type,  # entry are remove on inactive
        }

    return result