import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DB_URL"))
}

# Allow Django + React (localhost / dev servers)
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# CORS (so frontend can call API)
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = True  # still OK if you want cookies during dev

# CSRF (needed for Django admin login & forms)
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

# Cookies – in dev we keep them insecure
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False   # can read session in JS if needed
CSRF_COOKIE_HTTPONLY = False

# Static & Media – Dropbox config is unusual for local dev,
# normally you'd use local storage, but keeping your setup:
DEFAULT_FILE_STORAGE = "storages.backends.dropbox.DropBoxStorage"
STATICFILES_STORAGE = "storages.backends.dropbox.DropboxStorage"

# MEDIA_URL = "/media/"
MEDIA_URL = "https://www.dropbox.com/home/"
STATIC_URL = "/static/"
