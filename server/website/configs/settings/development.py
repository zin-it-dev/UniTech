from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("SECRET_KEY")

ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = ["*"]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": path.join(path.join(BASE_DIR, "database"), "unitech.db"),
    }
}

CORS_ALLOW_ALL_ORIGINS = True
