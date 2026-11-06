"""Production settings. Required operational values fail closed when absent."""

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

DEBUG = False
# Identity-document collection remains closed until legal approval and encrypted storage exist.
PROVIDER_ONBOARDING_ENABLED = False
PROVIDER_DOCUMENT_UPLOAD_ENABLED = False

_required = (
    "DJANGO_SECRET_KEY",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "DJANGO_ALLOWED_HOSTS",
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "EMAIL_HOST",
    "EMAIL_FROM",
)
_missing = [name for name in _required if not env.str(name, default="").strip()]  # noqa: F405
if _missing:
    raise ImproperlyConfigured(
        "Configuração de produção incompleta. Variáveis obrigatórias ausentes: "
        + ", ".join(_missing)
    )

if env.str("DB_ENGINE", default="mysql").strip().lower() != "mysql":  # noqa: F405
    raise ImproperlyConfigured("A configuração de produção da BICO exige MySQL.")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")  # noqa: F405
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS")  # noqa: F405
if "*" in ALLOWED_HOSTS:
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS não pode conter '*'.")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env.str("EMAIL_HOST")  # noqa: F405
EMAIL_PORT = env.int("EMAIL_PORT", default=587)  # noqa: F405
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="")  # noqa: F405
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="")  # noqa: F405
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)  # noqa: F405
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)  # noqa: F405
if EMAIL_USE_TLS and EMAIL_USE_SSL:
    raise ImproperlyConfigured("Configure somente uma opção entre EMAIL_USE_TLS e EMAIL_USE_SSL.")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)  # noqa: F405
SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=0)  # noqa: F405
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(  # noqa: F405
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False
)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=False)  # noqa: F405
