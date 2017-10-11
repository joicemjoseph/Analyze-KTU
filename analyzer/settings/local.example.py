"""
Local Settings
This file is to be renamed 'local.py', this file is in the .gitignore

For local/development change to:  from .development import *
For staging change to:            from .staging import *
For production change:            from .production import *
"""
from .development import *

SECRET_KEY = 'h(cdt=eg_55ebusoz%iqkm&dqemkr0biex=mr^gtr)r7r1gvog'
ALLOWED_HOSTS = ['127.0.0.1','localhost', 'testserver']
# APPS = ('your_apps',)
INSTALLED_APPS +=  [
    'debug_toolbar',
]
MIDDLEWARE_CLASSES += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
]
INTERNAL_IPS = ['127.0.0.1', 'localhost']

DEBUG_TOOLBAR_PANELS = [
        'template_timings_panel.panels.TemplateTimings.TemplateTimings',
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
]
INSTALLED_APPS +=   [
        'template_timings_panel',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#DEBUG_TOOLBAR = url(r'^__debug__/', include(debug_toolbar.urls))
# DATABASES= {}
# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # I always add this handler to facilitate separating loggings
        'log_file':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(VAR_ROOT, 'logs/django.log'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['log_file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'apps': { # I keep all my of apps under 'apps' folder, but you can also add them one by one, and this depends on how your virtualenv/paths are set
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    # you can also shortcut 'loggers' and just configure logging for EVERYTHING at once
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    },
}
