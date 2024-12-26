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

MIDDLEWARE += ["whitenoise.middleware.WhiteNoiseMiddleware"]

CORS_ALLOWED_ORIGINS = []
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

USE_X_FORWARDED_HOST = True

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
