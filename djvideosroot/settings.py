"""
Django settings for djvideosroot project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=1tnd40-opy5!d4u6wk6sl=b_yiyf_@8iyox5v2-56&r_z$vvu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'videos',
    'celery',
    'django_celery_progressbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djvideosroot.urls'

UNPOPULAR_COUNT = 15
RAW_FILE_FOLDER = 'P:/Diziler/Legion/'
A_VIDEO_FOLDER = 'P:/Diziler/Vikings/'
B_VIDEO_FOLDER = 'P:/Diziler/The Gifted/'
M_VIDEO_FOLDER = 'P:/Diziler/Criminal Minds/'
P_VIDEO_FOLDER = 'P:/Diziler/Supergirl/'
U_VIDEO_FOLDER = 'P:/Diziler/Doctor Who/'
VIDEO_PATHS = [A_VIDEO_FOLDER, B_VIDEO_FOLDER, M_VIDEO_FOLDER, P_VIDEO_FOLDER, U_VIDEO_FOLDER, ]
LOG_NAME = BASE_DIR / 'djvideos_convert.log'

STATICFILES_DIRS = [
    ("/static", BASE_DIR / "static"),
    ("/css", BASE_DIR / "static/css"),
    ("/js", BASE_DIR / "static/js"),
    ("/webfonts", BASE_DIR / "static/webfonts"),
    ("/Raw", RAW_FILE_FOLDER),
    ("/Ordinary", A_VIDEO_FOLDER),
    ("/LGBT", B_VIDEO_FOLDER),
    ("/Movie", M_VIDEO_FOLDER),
    ("/Popular", P_VIDEO_FOLDER),
    ("/Unpopular", U_VIDEO_FOLDER),
]

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', ],
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

WSGI_APPLICATION = 'djvideosroot.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = 'P:/Diziler/'
MEDIA_URL = '/media'

global_filter = ""

# CELERY_BROKER_URL = 'amqp://localhost'
