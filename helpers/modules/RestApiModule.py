from core import DataFileManager
from helpers.modules.BaseModule import BaseModule

import requests
import time


class RestApiModule(BaseModule):
    _baseUrl = ''
    _hostname = ''
    _port = 80
    _protocol = 'http'
    _token = None

    def internal_init(self):
        super().internal_init()
        self._loadToken()

    def _send(self, url, method='get', *args, **kwargs):
        handler = getattr(requests, method.lower())

        def call_try(handler, *args, **kwargs):
            try:
                return handler(*args, **kwargs)
            except requests.exceptions.ConnectionError:  # network problem
                time.sleep(10)
                return call_try(handler, *args, **kwargs)

        return call_try(handler, url, *args,**kwargs)


    def _getUrl(self, page):
        if self._baseUrl:
            page = '%s/%s' % (self._baseUrl, page)

        return '%s://%s:%d/%s' % (self._protocol, self._hostname, self._port, page)

    def _deleteToken(self):
        self._token = DataFileManager.delete(self.module_name, 'token')

    def _loadToken(self):
        self._token = DataFileManager.load(self.module_name, 'token')

    def _saveToken(self):
        DataFileManager.save(self.module_name, 'token', self._token)
