"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : Project Base Settings
"""

# System
import os
from pathlib import Path

# Project
from core.constants import SERVICE


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = SERVICE.SECRET_KEY

DEBUG = SERVICE.DEBUG

ALLOWED_HOSTS = ["*"]


# ==================================================================== #
#                     설치된 앱, 사용하는 앱 config                         #
# ==================================================================== #

LOCAL_APPS = [
    "apps",
    "apps.users",
    "apps.short_url",
    "core",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "django_harlequin",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"

APPEND_SLASH = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # 프로젝트에 전반적으로 사용되는 템플릿이 있다면 여기에서 설정
            # 이렇게 하면은 이제 templates 특정 앱 안에 두게 되는데 특정 앱이 아닌 앱에서 벗어난 경로에 templates 파일은 이렇게 설정해줘야 한다.
            os.path.join(BASE_DIR, "config", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"

AUTH_USER_MODEL = "users.User"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"  # 언어 - 국가 설정

TIME_ZONE = "Asia/Seoul"  # 시간대 설정

USE_I18N = True  # 국제화

USE_L10N = True  # 지역화, 4.0 부터 더 이상 사용되지 않는다. (https://docs.djangoproject.com/en/4.2/ref/settings/#use-l10n)

USE_TZ = False  # 장고 시간대 사용 여부


# ==================================================================== #
#                  file system (static) config                         #
# ==================================================================== #
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# ==================================================================== #
#                       DRF config                                     #
# ==================================================================== #
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("core.jwt.CustomJWTAuthentication",),  # 애플리케이션에서 사용할 인증 방법을 정의  # JWT 인증 방식
    "EXCEPTION_HANDLER": "core.exception.default_exception_handler",  # 예외 처리기 설정
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",  # drf의 schema 클래스를 drf-spectacular의 AuthSechema로 교체
    "DEFAULT_PARSER_CLASSES": [  # 요청 본문을 파싱하는 데  사용할 파서를 지정
        "rest_framework.parsers.JSONParser",  # JSON 파서
    ],
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    # "DEFAULT_RENDERER_CLASSES": ("core.renderers.CustomRenderer",),
    "DEFAULT_RESPONSE_CLASS": "core.response.CustomResponse",
    "DEFAULT_PAGINATION_CLASS": "core.pagination.CustomPagination",
}

# ==================================================================== #
#                       Logging config                                 #
# ==================================================================== #
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "django.server": {
            "format": "[%(asctime)s] %(levelname)s [PID: %(process)d - %(processName)s] | [TID: %(thread)d - %(threadName)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
            "formatter": "django.server",
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
