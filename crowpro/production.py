import random
import string
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()
SECRET_KEY = "".join(random.choices(string.ascii_letters +
                                    string.digits,
                                    k=20))

ALLOWED_HOSTS = ['.vercel.app', 'now.sh', '138.68.137.234', '.santosh-bhattarai.com.np']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv("POSTGRES_DATABASE"),
#         'USER': os.getenv("POSTGRES_USER"),
#         'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
#         'HOST': os.getenv("POSTGRES_HOST"),
#     }
# }

DATABASES = {
    'default': dj_database_url.config(default=os.getenv("DB_URL"))
}

CORS_ALLOWED_ORIGINS = [
    "https://api.santosh-bhattarai.com.np",
    "https://www.santosh-bhattarai.com.np",
    "https://santosh-bhattarai.com.np",
    "http://127.0.0.1:3000"
]

CSRF_TRUSTED_ORIGINS = [
    "https://api.santosh-bhattarai.com.np",
    "https://www.santosh-bhattarai.com.np",
    "https://santosh-bhattarai.com.np",
    "http://127.0.0.1:3000"
]

CORS_ORIGINS_WHITELIST = [
    "https://api.santosh-bhattarai.com.np",
    "https://www.santosh-bhattarai.com.np",
    "https://santosh-bhattarai.com.np",
    "http://127.0.0.1:3000"

]

CORS_ALLOW_CREDENTIALS = True


