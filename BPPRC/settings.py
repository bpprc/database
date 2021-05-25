from dotenv import load_dotenv
from celery.schedules import crontab
import os

"""
Django settings for BPPRC project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# env
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", '4s3l2tsgm_j4gr0hs5c^_x&vnlhf3e@tyiib73vs&uk3up#7&$')

if os.environ.get('DEVELOPMENT'):
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'camtech-bpp.test.ifas.ufl.edu',
                 'camtech-bpp.ifas.ufl.edu']
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if os.environ.get('DATABASE_TYPE') == 'sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'proteindatabase_test',
            'USER': 'suresh',
            'PASSWORD': 'pannerselvam123',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'BPPRC.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'BPPRC.wsgi.application'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'clustalanalysis',
    'bestmatchfinder',
    'database',
    'namingalgorithm',
    'captcha',
    'graphs',
    'crispy_forms',
    'django_tables2',
    'import_export',
    'extra',
    'django_ses',
    'django_celery_beat',
    'association',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.twitter',
    # 'allauth.socialaccount.providers.yahoo',
    # 'allauth.socialaccount.providers.linkedin',
]


SITE_ID = 1

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"


STATICFILES_DIRS = (os.path.join(BASE_DIR, 'stat'), )

# print("MEDIA_URL", "/media/")
# print("MEDIA_ROOT", os.path.join(BASE_DIR, 'media'))
# print("STATIC_ROOT", os.path.join(BASE_DIR, "static"))
# print("STATIC_URL", '/static/')
# path for temp folder
TEMP_DIR = os.path.join(BASE_DIR, "tmp")

# Number of days to keep temp files
TEMP_LIFE = 5

NEEDLE_PATH = os.environ.get('NEEDLE_PATH', '')
BLAST_PATH = os.environ.get('BLAST_PATH', '')
CLUSTAL_PATH = os.environ.get('CLUSTAL_PATH', '')

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + "/logs/djangologfile.log",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'bestmatchfinder': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}

ADMIN_REORDER = [
    {'app': 'database', 'models': (
        {'model': 'database.Description', 'label': 'Category Descriptions'},
        {'model': 'database.PesticidalProteinDatabase', 'label': 'Public Sequences'},
        {'model': 'database.PesticidalProteinPrivateDatabase',
            'label': 'Private Sequences'},
        {'model': 'database.StructureDatabase',
            'label': 'Structures'},
        {'model': 'database.PesticidalProteinHiddenSequence',
            'label': 'Hidden Sequences'},
        {'model': 'database.ProteinDetail', 'label': 'Three domain details'},
        {'model': 'database.OldnameNewnameTableRight',
            'label': 'Organized by Oldname'},
        {'model': 'database.OldnameNewnameTableLeft',
            'label': 'Organized by New name'})},
    'namingalgorithm',
    'extra',
    {'app': 'auth', 'models': (
        'auth.Group',
        {'model': 'auth.User', 'label': 'Staff'},
    )},
    'django_ses',
    'clustalanalysis',
    'association',
    'sites',
    'auth'
    'account',
    'socialaccount',
]

# SESSION
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_SAVE_EVERY_REQUEST = True

# ? import and export ?
TRACK_AJAX_REQUESTS = True
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE') == 'True'
CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = ['camtech-bpp.ifas.ufl.edu',
                        'camtech-bpp.test.ifas.ufl.edu', 'ifs-ent-camtech2.ifas.ufl.edu']

CRISPY_TEMPLATE_PACK = os.environ.get('CRISPY_TEMPLATE_PACK')

# All auth
# ACCOUNT_USERNAME_REQUIRED = True
# ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
# ACCOUNT_UNIQUE_EMAIL = True
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/submit/'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_BLACKLIST = ["Neil", "Colin", "god", "admin"]
ACCOUNT_USERNAME_MIN_LENGTH = 2
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_FORM_CLASS = 'extra.forms.SignupForm'
# ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# SOCIAL_AUTH_TWITTER_KEY = 'x2FGb9GkeaGFBTCFxU1VSDDdv'
# SOCIAL_AUTH_TWITTER_SECRET = 'cANYB7UKeTtq0FGYuyChwVROqpkV4vr6EMMit9sBUNiWrfJZyJ'


# AWS US@entomology2021
# EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_SES_REGION_NAME = os.environ.get('AWS_SES_REGION_NAME')
# AWS_SES_REGION_ENDPOINT = os.environ.get('AWS_SES_REGION_ENDPOINT')

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = os.environ.get('AWS_ACCESS_KEY_ID')
# EMAIL_HOST_PASSWORD = os.environ.get('AWS_SECRET_ACCESS_KEY')
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = '<bpprc.database@gmail.com>'

# gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'bpprc.database@gmail.com'
EMAIL_HOST_PASSWORD = 'US@entomology2021'

# google reCAPTCHA
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

# celery
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'US/Eastern'

# other celery settings
# CELERY_BEAT_SCHEDULE = {
#     'check_new_submission': {
#         'task': 'namingalgorithm.tasks.check_new_submission',
#         'schedule': crontab(minute=28, hour=12),
#     }
# }
