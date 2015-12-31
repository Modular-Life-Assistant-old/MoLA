from core import Log, EventManager, ModuleManager


class InternalBaseModel:
    """This class implement the internal methods needed by modules."""
    name = 'NO_NAME'
    name_prefix = ''

    def __getitem__(self, name):
        if name == 'name' and self.name_prefix:
            return '%s_%s' % (self.name_prefix, self.name)

        if not hasattr(self, name):
            raise AttributeError

        return getattr(self, name)

    def add_crash(self, text, *args, **kwargs):
        """Add a crash message to logger"""
        text = '%s %s: %s' % (self.name_prefix, self.name, text)
        Log.crash(text, *args, **kwargs)

    def add_critical(self, text, *args, **kwargs):
        """Add a critical message to logger"""
        text = '%s %s: %s' % (self.name_prefix, self.name, text)
        Log.warning(text, *args, **kwargs)

    def add_debug(self, text, *args, **kwargs):
        """Add a debug message to logger"""
        text = '%s %s: %s' % (self.name_prefix, self.name, text)
        Log.debug(text, *args, **kwargs)

    def add_error(self, text, *args, **kwargs):
        """Add a error message to logger"""
        text = '%s %s: %s' % (self.name_prefix, self.name, text)
        Log.error(text, *args, **kwargs)

    def add_info(self, text, *args, **kwargs):
        """Add a message to logger"""
        text = '%s %s: %s' % (self.name_prefix, self.name, text)
        Log.info(text, *args, **kwargs)

    def add_warning(self, text, *args, **kwargs):
        """Add a warning message to logger"""
        text = '%s %s: %s' % (self.name_prefix, self.name, text)
        Log.warning(text, *args, **kwargs)

    def call(self, module_name, method_name, *arg, **kwargs):
        """call a method of other module."""
        return ModuleManager.call(module_name, method_name, *arg, **kwargs)

    def fire(self, event_name, *args, **kwargs):
        """Fire an Event."""
        kwargs['source'] = self
        return EventManager.fire(EventManager.Event(event_name, *args, **kwargs))

    def init(self):
        pass

    def notify(self, msg, image=None, sound=None):
        """Notify the owner."""
        return self.fire('notification', msg=msg, image=image, sound=sound)

    def _internal_init(self):
        self.init()

        # automatic register event handlers
        for event_handler in [h for h in dir(self) if h.endswith('_event')]:
            event_name = '_'.join(event_handler.split('_')[:-1])
            EventManager.register(event_name, getattr(self, event_handler))
