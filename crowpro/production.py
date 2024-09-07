import random
import string
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = "".join(random.choices(string.ascii_letters +
                                    string.digits,
                                    k=20))

ALLOWED_HOSTS = ['.vercel.app', 'now.sh', 'localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("POSTGRES_DATABASE"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'HOST': os.getenv("POSTGRES_HOST"),
        'PORT': os.getenv("POSTGRES_PORT"),
    }
}

CORS_ALLOWED_ORIGINS = [
    os.getenv("DEVELOPMENT_HOST"),
    "https://crowcrows-605q582yu-besoft33s-projects.vercel.app",
    "https://crowcrows-web-besoft33s-projects.vercel.app",
    "https://www.santosh-bhattarai.com.np"
]

CSRF_TRUSTED_ORIGINS = [
    os.getenv("DEVELOPMENT_HOST"),
    "https://crowcrows-605q582yu-besoft33s-projects.vercel.app",
    "https://crowcrows-web-besoft33s-projects.vercel.app",
    "https://www.santosh-bhattarai.com.np"
]

CORS_ORIGINS_WHITELIST = [
    os.getenv("DEVELOPMENT_HOST"),
    "https://crowcrows-605q582yu-besoft33s-projects.vercel.app",
    "https://crowcrows-web-besoft33s-projects.vercel.app",
    "https://www.santosh-bhattarai.com.np"
]

CORS_ALLOW_CREDENTIALS = True

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
