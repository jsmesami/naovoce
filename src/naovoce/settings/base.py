import os

from django.contrib.messages import constants as messages


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

DEBUG = False
THUMBNAIL_DEBUG = DEBUG

COMPRESS_ENABLED = True

ALLOWED_HOSTS = '.na-ovoce.cz', '.na-ovoce.cz.'

SECRET_KEY = None  # must be set in instance-specific settings/local.py

ADMINS = MANAGERS = (
    ('Ondra Nejedlý', 'software@na-ovoce.cz'),
)

DEFAULT_FROM_EMAIL = 'registration@na-ovoce.cz'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'naovoce',
        'CONN_MAX_AGE': 600,
        'USER': '',      # must be set in instance-specific settings/local.py
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:{home}/memcached.sock'.format(home=os.path.expanduser('~')),
        'TIMEOUT': 60 * 60 * 24,  # 1 day
    },
    'fruit': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:{home}/memcached.sock'.format(home=os.path.expanduser('~')),
        'TIMEOUT': None,
        'KEY_PREFIX': 'fruit',
    }
}

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

TIME_ZONE = None  # set the TZ to system value (on Unix)

LANGUAGE_CODE = 'en'

MODELTRANSLATION_DEFAULT_LANGUAGE = 'cs'

LANGUAGES = (
    ('en', 'English'),
    ('cs', 'Česky'),
)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'naovoce/media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'naovoce/static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

THUMBNAIL_PREFIX = 'CACHE/thumbnails/'

LOCALE_PATHS = os.path.join(PROJECT_ROOT, 'locale'),

ROOT_URLCONF = 'naovoce.urls'

WSGI_APPLICATION = 'naovoce.wsgi.application'

SSL_ENABLED = True
SECURE_HSTS_SECONDS = 60*10  # TODO
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

AUTH_USER_MODEL = 'user.FruitUser'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_ADAPTER = 'user.social.SocialAccountAdapter'
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email'],
        'VERIFIED_EMAIL': True,
        'FIELDS': (
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
        ),
        'EXCHANGE_TOKEN': True,
        'VERSION': 'v2.4'
    }
}

COMPRESS_CSS_FILTERS = (
    'compressor.filters.cssmin.CSSMinFilter',
)

COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', 'lessc {infile} {outfile}'),
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MESSAGE_TAGS = {
    messages.SUCCESS: 'success alert-success',
    messages.INFO: 'info alert-info',
    messages.DEBUG: 'debug alert-info',
    messages.WARNING: 'warning alert-warning',
    messages.ERROR: 'error alert-danger',
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'naovoce/templates')],
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'naovoce.context_processors.common',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.i18n.middleware.SessionBasedLocaleMiddleware',
)

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
)

LOCAL_APPS = (
    'user',
    'gallery',
    'blog',
    'fruit',
    'fruit.herbarium',
    'staticpage',
    'utils',
    'utils.i18n',
    'comments',
    'naovoce',
)

EXTERNAL_APPS = (
    'sorl.thumbnail',
    'modeltranslation',
    'compressor',
    'bootstrapform',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'endless_pagination',
    'rest_framework',
    'rest_framework.authtoken',
)

ADMIN_APPS = (
    'djamin',
    'django.contrib.admin',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(process)d %(message)s',
        },
    },
    'filters': {
        'debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'verbose',
            'address': '/dev/log',
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'naovoce': {
            'level': 'DEBUG',
            'handlers': ['syslog', 'console'],
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}
