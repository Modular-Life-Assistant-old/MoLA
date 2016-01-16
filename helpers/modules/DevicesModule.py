import time

from core import DataFileManager
from helpers.modules.BaseModule import BaseModule
from helpers.network import get_arp_infos


class DevicesModule(BaseModule):
    devices = {}
    device_class = None
    wait_next_update = 5

    def add_device(self, *args, **kwargs):
        """Add a device

        :param device_object: device object
        :return: is successful added
        """
        if not hasattr(self.device_class, '__call__'):
            raise TypeError('device_class is not callable')

        device_object = self.device_class(*args, **kwargs)
        self.devices[device_object.name] = device_object
        self.save_config()
        return True

    def del_device(self, device_object_or_name):
        """Remove a device

        :param device_object_or_name:
        :return: is successful deleted
        """
        if isinstance(device_object_or_name, str):
            del(self.devices[device_object_or_name])
            return True

        for name, device in self.devices.items():
            if device_object_or_name == device:
                del(self.devices[name])
                self.save_config()
                return True

    def device_on_network(self, ip, mac):
        """Device are detected on network (called by search_devices)

        :param ip: ip adress
        :param mac: mac adress
        """

    def _internal_init(self):
        super(DevicesModule, self)._internal_init()
        self.search_devices()

    def load_config(self):
        """Load device from config file"""
        for device in DataFileManager.load(self.name, 'devices', []):
            self.add_device(*device['args'], **device['kwargs'])

    def run(self):
        """This module loop running."""
        while self.is_running:
            for device in self.devices.values():
                device.update()
            time.sleep(self.wait_next_update)

    def save_config(self):
        """Save devices in config file."""
        devices_conf = []

        for device in self.devices.values():
            config = device.get_config()
            if len(config):
                devices_conf.append(config)

        DataFileManager.save(self.name, 'devices', devices_conf)

    def search_devices(self):
        """Search all devices on network."""
        for ip, infos in get_arp_infos().items():
            if infos['is_dynamic']:
                self.device_on_network(ip, infos['mac'])
