import uuid
import warnings

from django.core.exceptions import ValidationError
from PIL import Image, ImageFilter, ImageOps, ImageStat, UnidentifiedImageError

MAX_DOCUMENT_SIZE = 8 * 1024 * 1024
MIN_DOCUMENT_WIDTH = 800
MIN_DOCUMENT_HEIGHT = 500
MAX_DOCUMENT_PIXELS = 25_000_000
ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}


def document_upload_path(instance, filename):
    extension = {
        "JPEG": ".jpg",
        "PNG": ".png",
        "WEBP": ".webp",
    }.get(getattr(instance, "detected_format", ""), ".bin")
    return (
        f"provider-verification/{instance.application_id}/{instance.side.lower()}/"
        f"{uuid.uuid4().hex}{extension}"
    )


def validate_document_file(upload):
    if not upload:
        return
    if upload.size > MAX_DOCUMENT_SIZE:
        raise ValidationError("Cada imagem deve ter no máximo 8 MB.")

    try:
        upload.seek(0)
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            image = Image.open(upload)
            detected_format = image.format
            width, height = image.size
            image.verify()

        if detected_format not in ALLOWED_IMAGE_FORMATS:
            raise ValidationError("Envie a foto em JPG, PNG ou WebP.")
        if width * height > MAX_DOCUMENT_PIXELS:
            raise ValidationError("A imagem excede a resolução máxima permitida.")
        if min(width, height) < MIN_DOCUMENT_HEIGHT or max(width, height) < MIN_DOCUMENT_WIDTH:
            raise ValidationError(
                "A imagem precisa ter pelo menos 800 × 500 pixels. Fotografe o documento de perto."
            )

        upload.seek(0)
        with Image.open(upload) as source:
            image = ImageOps.exif_transpose(source).convert("RGB")
            image.thumbnail((512, 512))
            gray = ImageOps.grayscale(image)
            luminance = ImageStat.Stat(gray).mean[0]
            if luminance < 38:
                raise ValidationError(
                    "A foto está muito escura. Use iluminação uniforme, "
                    "sem sombras sobre o documento."
                )

            edge_deviation = ImageStat.Stat(gray.filter(ImageFilter.FIND_EDGES)).stddev[0]
            if edge_deviation < 5.0:
                raise ValidationError(
                    "A foto parece desfocada ou sem detalhes. Limpe a lente e fotografe novamente."
                )

            # This catches nearly uniform/blank images without claiming OCR or identity checks.
            contrast = ImageStat.Stat(gray).stddev[0]
            if contrast < 5.0:
                raise ValidationError(
                    "Não foi possível identificar detalhes na foto. "
                    "Envie uma imagem nítida do documento."
                )
        upload.detected_format = detected_format
    except ValidationError:
        raise
    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ):
        raise ValidationError("O arquivo não é uma imagem válida ou está danificado.") from None
    finally:
        try:
            upload.seek(0)
        except (AttributeError, OSError):
            pass
