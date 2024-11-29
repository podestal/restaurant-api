from .base import *

DEBUG = True
ALLOWED_HOSTS.extend(filter(None, os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")))

# Use PostgreSQL for production
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
    }
}

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware", "whitenoise.middleware.WhiteNoiseMiddleware"]

INTERNAL_IPS = ["127.0.0.1"]

CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]
CORS_ALLOWED_ORIGINS.extend(
    filter(None, os.environ.get("DJANGO_CORS_ALLOWED_ORIGINS", "").split(","))
)

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    'Session-ID',
]

CSRF_TRUSTED_ORIGINS = []
CSRF_TRUSTED_ORIGINS.extend(
    filter(None, os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(","))
)

# Email settings for Zoho Mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587  # Use 465 for SSL
EMAIL_USE_TLS = True  # Set False if using SSL, and use EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'l.r.p.2991@gmail.com' # Example: 'your-email@yourdomain.com'
EMAIL_HOST_PASSWORD = '13anguloX'
