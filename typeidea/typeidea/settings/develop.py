from .base import * # NOQA

DEBUG=True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'devdb.sqlite3'),
    }
}

STATIC_ROOT = "/tmp/static/"

# 用于url上面显示加载静态资源路径
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "themes", THEME, 'static'),
]