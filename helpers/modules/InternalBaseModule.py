from core import Log, ModuleManager, NotificationManager
from core.settings import MODULES_PATH

import gettext
import locale
import os


class InternalBaseModule:
    """This class implement the internal methods needed by modules."""
    module_name = ''
    is_running = False
    _translate = None

    def add_crash(self, text, *args, **kwargs):
        """Add a crash message to logger"""
        Log.crash('module %s: %s' % (self.module_name, text), *args, **kwargs)

    def add_critical(self, text, *args, **kwargs):
        """Add a critical message to logger"""
        Log.warning('module %s: %s' % (self.module_name, text), *args, **kwargs)

    def add_debug(self, text, *args, **kwargs):
        """Add a debug message to logger"""
        Log.debug('module %s: %s' % (self.module_name, text), *args, **kwargs)

    def add_error(self, text, *args, **kwargs):
        """Add a error message to logger"""
        Log.error('module %s: %s' % (self.module_name, text), *args, **kwargs)

    def add_info(self, text, *args, **kwargs):
        """Add a message to logger"""
        Log.info('module %s: %s' % (self.module_name, text), *args, **kwargs)

    def add_warning(self, text, *args, **kwargs):
        """Add a warning message to logger"""
        Log.warning('module %s: %s' % (self.module_name, text), *args, **kwargs)

    def call(self, module_name, method_name, *arg, **kwargs):
        """call a method of other module."""
        return ModuleManager.call(module_name, method_name, *arg, **kwargs)

    def internal_init(self):
        self.init()

    def notify(self, msg):
        """Notify the owner."""
        return NotificationManager.notify(self.module_name, msg)

    def _(self, key):
        """Get translated string."""
        if not self._translate:
            # windows os language detection fix (for gettext)
            if os.name == 'nt':
                try:
                    import ctypes

                    # get all locales using windows API
                    lcid_user = ctypes.windll.kernel32.GetUserDefaultLCID()
                    lcid_system = ctypes.windll.kernel32.GetSystemDefaultLCID()

                    if lcid_user != lcid_system:
                        lcids = [lcid_user, lcid_system]
                    else:
                        lcids = [lcid_user]

                    langs = filter(None, [locale.windows_locale.get(i) for i in lcids]) or None

                except ImportError:
                    langs = [locale.getdefaultlocale()[0]]

                os.environ['LANGUAGE'] = ':'.join(langs)

            self._translate = gettext.translation(
                'module',
                localedir=os.path.join(MODULES_PATH, self.module_name, 'locale')
            )

        return self._translate.gettext(key)
