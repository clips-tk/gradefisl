from settings import MIDDLEWARE_CLASSES, INSTALLED_APPS

import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS = list(INSTALLED_APPS)
MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)

# Django debug toolbar
INTERNAL_IPS = ('127.0.0.1',)
MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')
INSTALLED_APPS.extend(['debug_toolbar', 'debug_toolbar_htmltidy'])
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    'debug_toolbar_htmltidy.panels.HTMLTidyDebugPanel',
)

# django nose
INSTALLED_APPS.append('django_nose')
SOUTH_TESTS_MIGRATE = False
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ('-s', '--rednose',)

# tests in memory
if 'test' in sys.argv:
    DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
        }
    }
