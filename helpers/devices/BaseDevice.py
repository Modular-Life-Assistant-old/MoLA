from helpers.devices.InternalBaseDevice import InternalBaseDevice


class BaseDevice(InternalBaseDevice):
    """This class is a template of methods to be implemented by devices."""
    def is_available(self):
        """This device is available ?"""
        return True

    def init(self):
        """This device has been initialized"""
        pass

    def get_config(self):
        """Get config info to save (passed on constructor on restart)

        :return: list of object parameters
        """
        return {'args': [], 'kwargs': {}}

    def run(self):
        """This device loop running."""
        pass

    def started(self):
        """This device has been started."""
        pass

    def stopped(self):
        """This device has been stopped."""
        pass

    def update(self):
        """This device update."""
        pass