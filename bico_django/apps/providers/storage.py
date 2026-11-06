import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken, MultiFernet
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible


@deconstructible
class PrivateDocumentStorage(FileSystemStorage):
    """Filesystem storage that deliberately has no public URL interface."""

    def __init__(self):
        super().__init__(
            location=settings.PRIVATE_MEDIA_ROOT,
            base_url=None,
            file_permissions_mode=0o600,
            directory_permissions_mode=0o700,
        )

    @staticmethod
    def _cipher():
        configured_keys = getattr(settings, "PROVIDER_DOCUMENT_ENCRYPTION_KEYS", [])
        if configured_keys:
            try:
                return MultiFernet([Fernet(key.encode("ascii")) for key in configured_keys])
            except (ValueError, TypeError):
                raise ImproperlyConfigured(
                    "BICO_PROVIDER_DOCUMENT_ENCRYPTION_KEYS contém uma chave inválida."
                ) from None
        if settings.DEBUG:
            # Local development only: derive from the high-entropy Django secret.
            key_bytes = hashlib.sha256(
                b"BICO:provider-document-storage:v1:" + settings.SECRET_KEY.encode("utf-8")
            ).digest()
            return Fernet(base64.urlsafe_b64encode(key_bytes))
        raise ImproperlyConfigured(
            "Configure BICO_PROVIDER_DOCUMENT_ENCRYPTION_KEYS antes de ler ou gravar documentos."
        )

    def save(self, name, content, max_length=None):
        if hasattr(content, "seek"):
            content.seek(0)
        plaintext = content.read()
        token = self._cipher().encrypt(plaintext)
        return super().save(name, ContentFile(token), max_length=max_length)

    def open(self, name, mode="rb"):
        if mode not in {"rb", "r"}:
            raise ValueError("Documentos privados só podem ser lidos pelo storage.")
        with super().open(name, "rb") as encrypted_file:
            encrypted = encrypted_file.read()
        try:
            plaintext = self._cipher().decrypt(encrypted)
        except InvalidToken:
            raise ImproperlyConfigured(
                "O arquivo privado não pôde ser descriptografado com as chaves configuradas."
            ) from None
        return ContentFile(plaintext, name=name)

    def url(self, name):
        raise ValueError("Documentos de identidade não possuem URL pública.")


private_document_storage = PrivateDocumentStorage()
