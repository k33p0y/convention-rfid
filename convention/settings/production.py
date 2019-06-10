from .base import *
from decouple import Csv

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        # 'OPTIONS': {
        #     # Tell MySQLdb to connect with 'utf8mb4' character set
        #     'charset': 'utf8mb4',
        # },
        # # Tell Django to build the test database with the 'utf8mb4' character set
        # 'TEST': {
        #     'CHARSET': 'utf8mb4',
        #     'COLLATION': 'utf8mb4_unicode_ci',
        # },
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}