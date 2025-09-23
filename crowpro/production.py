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

DATABASES = {
    'default': dj_database_url.config(default=os.getenv("DB_URL"))
}

CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
SESSION_COOKIE_DOMAIN = os.environ.get("SESSION_COOKIE_DOMAIN", "api.santoshbhattarai.com")
CSRF_COOKIE_DOMAIN = os.environ.get("CSRF_COOKIE_DOMAIN", "api.santoshbhattarai.com")
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')

CORS_ALLOW_CREDENTIALS = True


