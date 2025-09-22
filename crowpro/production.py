import random
import string
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()
SECRET_KEY = "".join(random.choices(string.ascii_letters +
                                    string.digits,
                                    k=20))
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

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
    "138.68.137.234",
    "https://santosh-bhattarai.com.np",
]
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')

CORS_ALLOW_CREDENTIALS = True


