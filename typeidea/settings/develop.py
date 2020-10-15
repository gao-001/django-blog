from .base import *  # NOQA

DEBUG =True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog_database',
        'USER': 'root',
        'PASSWORD': 'Nchu011230',
        'HOST': '127.0.0.1',
        'POST': 3306,
        'CONN_MAX_AGE':5*60,
        'OPTIONS':{'charset':'utf8mb4'},
    }
}
