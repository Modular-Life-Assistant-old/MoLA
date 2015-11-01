import time
from core import NotificationManager
from helpers.modules.BaseModule import BaseModule


class DevicesModule(BaseModule):
    devices = {}
    wait_next_update = 5

    def add_device(self, device_object, name=''):
        """Add a device

        :param device_object:
        :param name:
        """
        if not name:
            name = str(device_object)

        self.devices[name] = device_object

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
                return True

    def internal_init(self):
        super(DevicesModule, self).internal_init()
        devices = self.search_new()

        if not isinstance(devices, list):
            return

        for device in devices:
            self.add_device(device)

    def run(self):
        """This module loop running."""
        while self.is_running:
            for device in self.devices.values():
                device.update()
            time.sleep(self.wait_next_update)

    def search_new(self):
        """Search new devices

        :return: list of device object
        """
        return []