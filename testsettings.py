# test_settings.py
import os
from datetime import timedelta

DEBUG = True

SECRET_KEY = 'fake-key'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'juntagrico_godparent',
    'juntagrico',
    'fontawesomefree',
    'import_export',
    'impersonate',
    'adminsortable2',
    'polymorphic',
    'crispy_forms',
    'multiselectfield',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  'yourdatabasename.db',
    }
}

ROOT_URLCONF = 'testurls'

AUTHENTICATION_BACKENDS = (
    'juntagrico.util.auth.AuthenticateWithEmail',
    'django.contrib.auth.backends.ModelBackend'
)


MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware'
)

EMAIL_HOST = os.environ.get('JUNTAGRICO_EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('JUNTAGRICO_EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('JUNTAGRICO_EMAIL_PASSWORD')
EMAIL_PORT = os.environ.get('JUNTAGRICO_EMAIL_PORT', 2525)
EMAIL_USE_TLS = os.environ.get('JUNTAGRICO_EMAIL_TLS', False)


if DEBUG is True:
    # display all emails in console instead
    WHITELIST_EMAILS = [r'.*']
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

LANGUAGE_CODE = 'de'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

DATE_INPUT_FORMATS = ['%d.%m.%Y']

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


class InvalidTemplateVariable(str):
    def __mod__(self, other):
        raise NameError(f"In template, undefined variable or unknown value for: '{other}'")


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
            'string_if_invalid': InvalidTemplateVariable("%s"),
            'debug': True
        },
    },
]

LOGIN_REDIRECT_URL = "/"

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

IMPORT_EXPORT_EXPORT_PERMISSION_CODE = 'view'

ENABLE_SHARES = True

GODPARENT_CONTACT = 'godparent@juntagrico.juntagrico'
GODPARENT_SHOW_MENU = False
GODPARENT_MEMBERSHIP_DURATION_LIMIT = timedelta(weeks=52)
