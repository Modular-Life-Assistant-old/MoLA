from core import NotificationManager
from helpers.modules.BaseModule import BaseModule


class NotificationModule(BaseModule):
    def internal_init(self):
        super().internal_init()
        NotificationManager.register(self.module_name, self.send)

    def send(self, msg):
        """ Send message."""
        raise NotImplementedError()
