"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : Project Local Settings
"""

# Project
from config.django.base import *
from config.settings.swagger.settings import *
from core.constants import DATABASE

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DATABASE.DB_NAME,
        "USER": DATABASE.DB_USER,
        "PASSWORD": DATABASE.DB_PASSWORD,
        "HOST": DATABASE.DB_HOST,
        "PORT": DATABASE.DB_PORT,
        "TEST": {
            "NAME": DATABASE.DB_NAME,
        },
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
            "use_unicode": True,
        },
    }
}
