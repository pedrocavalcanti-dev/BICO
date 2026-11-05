from pathlib import Path
from urllib.parse import urlsplit

from django.core.exceptions import ValidationError

MAX_PUBLIC_IMAGE_BYTES = 5 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def validate_public_image(upload):
    extension = Path(upload.name).suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError("Envie uma imagem JPG, PNG ou WebP.")
    if upload.size > MAX_PUBLIC_IMAGE_BYTES:
        raise ValidationError("A imagem deve ter no máximo 5 MB.")


def validate_internal_destination(value):
    parsed = urlsplit(value)
    if (
        not value.startswith("/")
        or value.startswith("//")
        or "\\" in value
        or parsed.scheme
        or parsed.netloc
        or any(ord(character) < 32 for character in value)
    ):
        raise ValidationError("O destino do banner deve ser um caminho interno da BICO.")
