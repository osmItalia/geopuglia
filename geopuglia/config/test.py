# -*- coding: utf-8 -*-
'''
Test Configurations

- Runs in Debug mode
- Uses console backend for emails
- Use Django Debug Toolbar
'''
from configurations import values
from .common import Common


class Test(Common):

    # DEBUG
    DEBUG = values.BooleanValue(False)
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    # INSTALLED_APPS
    INSTALLED_APPS = Common.INSTALLED_APPS
    # END INSTALLED_APPS

    # Mail settings
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = values.Value('django.core.mail.backends.console.EmailBackend')
    # End mail settings


