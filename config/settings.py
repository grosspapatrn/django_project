from pathlib import Path
import environ

# loading .env file
env = environ.Env()
environ.Env.read_env(".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'project',
    'library',
    'TaskManager',
    'rest_framework',
    'shop',
    'django_filters'
]


# creating a global pagination class with max size at 6 objects
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 6
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# logging to save all system notifications into fileы
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# HTTP requests into http_logs.log
LOGGING['handlers']['http_file'] = {
    'class': 'logging.FileHandler',
    'filename': 'logs/http_logs.log',
}

LOGGING['loggers']['django.server'] = {
    'handlers': ['http_file'],
    'level': 'INFO',
    'propagate': False,
}


# SQL requests into db_logs.log
LOGGING['handlers']['db_file'] = {
    'class': 'logging.FileHandler',
    'filename': 'logs/db_logs.log',
}

LOGGING['loggers']['django.db.backends'] = {
    'handlers': ['db_file'],
    'level': 'DEBUG',
    'propagate': False,
}


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


DATABASE_ROUTER = env.bool('DATABASE_ROUTER', default=False)

if DATABASE_ROUTER:
    DATABASES = {
        'default': {
            'ENGINE': env('MYSQL_ENGINE'),
            'NAME': env('DATABASE_NAME'),
            'USER': env('MYSQL_USER'),
            'PASSWORD': env('MYSQL_PASSWORD'),
            'HOST': env('MYSQL_HOST'),
            'PORT': env('MYSQL_PORT')}}
else:
    DATABASES = {
        'default': {
            'ENGINE': env('SQLITE_ENGINE'),
            'NAME': BASE_DIR / env('SQLITE_NAME')}}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
