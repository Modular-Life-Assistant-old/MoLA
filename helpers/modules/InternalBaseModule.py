from core import Log, ModuleManager, NotificationManager
from core.settings import MODULES_PATH

import gettext
import locale
import os
import sys


class InternalBaseModule:
    """This class implement the internal methods needed by modules."""
    module_name = ''
    is_running = False
    _translate = None

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
