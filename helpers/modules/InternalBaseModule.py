from core.settings import MODULES_PATH
import gettext
import locale
import os

from helpers.InternalBaseModel import InternalBaseModel


class InternalBaseModule(InternalBaseModel):
    """This class implement the internal methods needed by modules."""
    is_running = False
    name_prefix = 'module'
    _translate = None

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
                localedir=os.path.join(MODULES_PATH, self.name, 'locale')
            )

        return self._translate.gettext(key)