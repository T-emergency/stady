"""
Django settings for stady project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import my_settings
from pathlib import Path
import os
from datetime import timedelta

# from telnetlib import AUTHENTICATION


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)4^yyofy5+cwk665st!cf43(9y@f-g8lajnc1y83l^+(!#%@cn'
# SECRET_KEY = my_settings.SECRET_KEY

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

    'django.contrib.sites',  # sns login

    # provider
    'corsheaders',
    # 'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # select google
    'allauth.socialaccount.providers.google',

    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'django_crontab',

    # service app
    'user',
    'study',
    'community',
    'study_group',
    'my_profile',
    'api',
    'blindcommunity'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:5500', 'http://localhost:5500']
CORS_ALLOW_CREDENTIALS = True


ROOT_URLCONF = 'stady.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'stady.wsgi.application'


# ????????? ???????????? ?????? ??????????????? ???

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     )
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication', ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE' : 6
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = my_settings.DATABASES


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
## Debug = True
# ?????? ??????
# STATIC_DIR = os.path.join(BASE_DIR, 'static')

# STATICFILES_DIRS = [
#     STATIC_DIR
#     # BASE_DIR / 'static',
# ]

STATIC_DIR = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [STATIC_DIR]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ??????????????? ??????
AUTH_USER_MODEL = 'user.User'

# ????????? ?????? ??????
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'splendent77@gmail.com'
EMAIL_HOST_PASSWORD = my_settings.EMAIL_KEY
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# sns login
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

LOGIN_REDIRECT_URL = '/'  # ?????? ????????? ????????? ????????????.

# Media files -???????????? ?????? url??? ???????????? ??????

# live server port 5500
CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:5500', 'http://localhost:5500']
# ?????? ?????? ??? ??????
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_ALL_ORIGINS = True


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30000),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=10000),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}



# LOGGING = {
#     'version': 1,	#logging ??????
#     'disable_existing_loggers': False, # ?????? ?????? ???????????? ????????? ?????? # ?????? True??? ???????????? ?????????? ???
#     'handlers': {					# ?????? ??????????????? ???????????? ?????? ???????????? ??????????????? ????????????????????? ???????????????, ?????? ?????????????????? ?????? ??????????????? ?????? 
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {				# ????????? console??? ????????? ... ????????? ????????? ?????? DEBUG????????? ????????? ????????? ??? ?????????, 
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     }
# }


CRONJOBS = [
    # 45??? ??????
    ('*/30 * * * *', 'study.cron.crontab_recent_check', '>> '+os.path.join(BASE_DIR, 'stady/log/cron.log')),
    #?????? 1 ???
    ('0 1 * * *', 'study_group.cron.crontab_penalty_student', '>> '+os.path.join(BASE_DIR, 'stady/log/cron.log')),
    # ?????? 2?????????
    ('0 2 * * *', 'study_group.recommend.create_recommand_csv', '>> '+os.path.join(BASE_DIR, 'stady/log/cron.log')),
    #?????? ????????? ?????? 3???
    ('0 3 * * 1', 'study_group.cron.crontab_week_penalty_reset', '>> '+os.path.join(BASE_DIR, 'stady/log/cron.log')),
]