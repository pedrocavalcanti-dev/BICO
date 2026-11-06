"""Local development settings. MySQL credentials come from the environment."""

from .base import *  # noqa: F403
from .base import BASE_DIR

DEBUG = env.bool("DJANGO_DEBUG", default=True)  # noqa: F405
PROVIDER_ONBOARDING_ENABLED = env.bool("BICO_PROVIDER_ONBOARDING_ENABLED", default=True)  # noqa: F405
PROVIDER_DOCUMENT_UPLOAD_ENABLED = env.bool(  # noqa: F405
    "BICO_PROVIDER_DOCUMENT_UPLOAD_ENABLED", default=True
)
ALLOWED_HOSTS = env.list(  # noqa: F405
    "DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1", "[::1]"]
)
INTERNAL_IPS = ["127.0.0.1"]
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / ".local-emails"
