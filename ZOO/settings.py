"""
Django settings for ZOO project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0(iz#y+(1-9ef69qo_dp7cx_9q6uu0m5_#*c%fetubd2gd4()w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',

    'rest_framework',
    'main.apps.MainConfig',
    'rest_framework_swagger',
    'django_filters',
    'ckeditor_uploader',

    'ckeditor',
    'import_export',

    'admin_reorder',
]

# REST_FRAMEWORK = {
#     'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
# }
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

ADMIN_REORDER = (
    # {
    #     'app': 'main',
    #     'label': 'Администрация сайта',  # название поля
    #     'models': [
    #         {'model': 'auth.User', 'label': 'Пользователи'},
    #     ]
    # },
    {
        'app': 'main',
        'label': 'База товаров интернет магазина',
        'models': [
            {'model': 'main.Product', 'label': 'Продукты'},
            {'model': 'main.Brand', 'label': 'Бренды'},
            {'model': 'main.Animal', 'label': 'Животные'},
            {'model': 'main.Category', 'label': 'Категории'},
        ]
    },
    {
        'app': 'main',
        'label': 'Заказы Товаров',
        'models': [
            {'model': 'main.Order', 'label': 'Заказы'},
            {'model': 'main.Customer', 'label': 'Покупатели'},
        ]
    },
    {
        'app': 'main',
        'label': 'Социальны',
        'models': [
            {'model': 'main.Comments', 'label': 'Отзыв о магазине'},
            {'model': 'main.InfoShop', 'label': 'Информация о магазине'},
            {'model': 'main.Consultation', 'label': 'Обратный звонок'},

        ]
    }
)

CORS_ALLOW_ALL_ORIGINS = True
ROOT_URLCONF = 'ZOO.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'ZOO.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'territory_zoo',
#         'USER': 'korney',
#         'PASSWORD': 'ygvuhb1989',
#         'HOST': 'localhost',
#         # 'PORT': '5432'
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CKEDITOR_UPLOAD_PATH = ''
CKEDITOR_CONFIGS = {
    'default': {
        'height': 150,
        'width': 900,
        'enterMode': 2,
        'skin': 'moono',
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'
                       ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',
    },
    'custom': {
        'height': 400,
        'width': 900,
        'enterMode': 2,
        'skin': 'moono',
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-',
                       'Bold', 'FontSize',
                       ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',
    }
}
