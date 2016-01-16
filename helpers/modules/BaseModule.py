from helpers.modules.InternalBaseModule import InternalBaseModule


class BaseModule(InternalBaseModule):
    """This class is a template of methods to be implemented by modules."""
    module_path = ''

    def cron_day(self):
        """This method has been called one time by day"""
        pass

    def cron_hour(self):
        """This method has been called one time by day."""
        pass

    def cron_min(self):
        """This method has been called one time by min."""
        pass

    def cron_month(self):
        """This method has been called one time by month."""
        pass

    def cron_week(self):
        """This method has been called one time by week."""
        pass

    def cron_year(self):
        """This method has been called one time by year."""
        pass

    def is_available(self):
        """This module is available ?"""
        return True

    def init(self):
        """This module has been initialized."""
        pass

    def load_config(self):
        """Load module config."""
        pass

    def run(self):
        """This module loop running."""
        pass

    def started(self):
        """This module has been started."""
        pass

    def stopped(self):
        """This module has been stopped."""
        pass
