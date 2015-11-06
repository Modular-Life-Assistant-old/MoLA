import time
from core import DataFileManager
from helpers.modules.BaseModule import BaseModule


class DevicesModule(BaseModule):
    devices = {}
    devices_class = None
    wait_next_update = 5

    def add_device(self, *args, **kwargs):
        """Add a device

        :param device_object: device object
        :return: is successful added
        """
        device_object = self.devices_class(*args, **kwargs)
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

    def internal_init(self):
        super(DevicesModule, self).internal_init()
        self.load_config()
        devices = self.search_new()

        for device in devices:
            self.add_device(device)

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

    def search_new(self):
        """Search new devices

        :return: list of device object
        """
        return []
