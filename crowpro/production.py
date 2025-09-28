import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

# Don’t generate a new SECRET_KEY on each run (will break sessions/tokens)
SECRET_KEY = os.getenv("SECRET_KEY")

DATABASES = {
    'default': dj_database_url.config(default=os.getenv("DB_URL"))
}

# Allow both root domain and API subdomain
ALLOWED_HOSTS = [
    "santoshbhattarai.com",
    "api.santoshbhattarai.com",
]

# CORS (frontend calls API)
CORS_ALLOWED_ORIGINS = [
    "https://santoshbhattarai.com",
]
CORS_ALLOW_CREDENTIALS = True

# CSRF (frontend form submissions / admin login)
CSRF_TRUSTED_ORIGINS = [
    "https://santoshbhattarai.com",
    "https://api.santoshbhattarai.com",
]

# Cookies should work across subdomain + root domain
SESSION_COOKIE_DOMAIN = ".santoshbhattarai.com"
CSRF_COOKIE_DOMAIN = ".santoshbhattarai.com"

# Security
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # keep False so frontend JS can read CSRF token if needed

# Static / Media (Dropbox)
DEFAULT_FILE_STORAGE = "storages.backends.dropbox.DropBoxStorage"
STATICFILES_STORAGE = "storages.backends.dropbox.DropboxStorage"

MEDIA_URL = "https://www.dropbox.com/home/"
STATIC_URL = "/static/"

# DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
# STATICFILES_STORAGE = 'storages.backends.dropbox.DropboxStorage'
# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.dropbox.DropboxStorage",
#     },
#     "staticfiles": {
#         "BACKEND": "storages.backends.dropbox.DropboxStorage",
#     }
# }

# URL configuration for serving media files
# MEDIA_URL = 'https://www.dropbox.com/home/media/'
# STATIC_URL = 'https://www.dropbox.com/home/staticfiles/'
