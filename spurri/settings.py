import os
import dj_database_url
from django.http import Http404

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

MEDIA_ROOT = "media"
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: change this before deploying to production!
SECRET_KEY = 'i+acxn5(akgsn!sr4^qgf(^m&*@+g1@u^t@=8s@axc41ml*f=s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'bootstrap3',
    'website',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'updown',
    'django_gravatar',
    'django.contrib.humanize',
    'django_comments',
    'tagging',
    'emoji',
    'csvimport.app.CSVImportConf',
    'django_tables2',
    #'allauth.socialaccount.providers.linkedin',
    #'allauth.socialaccount.providers.google',
    #'allauth.socialaccount.providers.facebook',
    #'allauth.socialaccount.providers.github',
)

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
)

ROOT_URLCONF = 'spurri.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'spurri.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

if 'DATABASE_URL' in os.environ:
    DEBUG = False
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME', 'blank')
    EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD', 'blank')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    GS_ACCESS_KEY_ID = os.environ.get('GS_ACCESS_KEY_ID', 'blank')
    GS_SECRET_ACCESS_KEY = os.environ.get('GS_SECRET_ACCESS_KEY', 'blank')
    GS_BUCKET_NAME = 'spurrifiles'
    DEFAULT_FILE_STORAGE = 'storages.backends.gs.GSBotoStorage'
    GS_QUERYSTRING_AUTH = False
    ROLLBAR = {
        'access_token': os.environ.get('ROLLBAR_ACCESS_TOKEN', '11111111111111111'),
        'environment': 'development' if DEBUG else 'production',
        'root': BASE_DIR,
        'exception_level_filters': [
            (Http404, 'warning')
        ]
    }
    import rollbar
    rollbar.init(**ROLLBAR)

# local dev needs to set SMTP backend or fail at startup
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"

LOGIN_REDIRECT_URL = "/profile/"

SOCIALACCOUNT_PROVIDERS = \
    {'linkedin':
      {'SCOPE': ['r_emailaddress'],
       'PROFILE_FIELDS': ['id',
                         'first-name',
                         'last-name',
                         'email-address',
                         'picture-url',
                         'public-profile-url']}}


SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
       {'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4'}}


SOCIALACCOUNT_PROVIDERS = \
    { 'google':
        { 'SCOPE': ['profile', 'email'],
          'AUTH_PARAMS': { 'access_type': 'online' } }}
          
        
# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.


# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

#for social auth
SOCIALACCOUNT_PROVIDERS = { 

'facebook':
   {'METHOD': 'oauth2',
    'SCOPE': ['email', 'public_profile', 'user_friends'],
    'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
    'FIELDS': [
        'id',
        'email',
        'name',
        'first_name',
        'last_name',
        'verified',
        'locale',
        'timezone',
        'link',
        'gender',
        'updated_time'],
    'EXCHANGE_TOKEN': True,
    'LOCALE_FUNC': 'path.to.callable',
    'VERIFIED_EMAIL': True,
    'VERSION': 'v2.4'}}