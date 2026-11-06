from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.utils import timezone

from apps.catalog.models import ServiceCategory, ServiceListing, ServiceListingImage
from apps.core.models import HomeBanner
from apps.providers.models import ProviderProfile

CATEGORIES = (
    ("Jardinagem", "jardinagem", True, False),
    ("Encanamento", "encanamento", True, False),
    ("Pintura", "pintura", True, False),
    ("Limpeza", "limpeza", True, False),
    ("Elétrica", "eletrica", True, False),
    ("Manutenção residencial", "manutencao-residencial", True, True),
    ("Tecnologia", "tecnologia", False, True),
    ("Mecânica", "mecanica", False, True),
    ("Montagem de móveis", "montagem-de-moveis", False, True),
    ("Fotografia", "fotografia", False, True),
    ("Design", "design", False, True),
    ("Reformas", "reformas", False, True),
)
INDIVIDUAL_NAMES = (
    "Alex Silva",
    "Beatriz Costa",
    "Caio Mendes",
    "Dani Ribeiro",
    "Elias Rocha",
    "Fernanda Alves",
    "Guilherme Nunes",
    "Helena Santos",
    "Igor Martins",
    "Joana Lima",
    "Kaique Souza",
    "Larissa Melo",
    "Mateus Prado",
    "Nina Barros",
    "Otávio Freire",
)
COMPANY_NAMES = ("Equipe Verde Serviços", "Casa em Ordem Serviços", "Oficina Horizonte")
SERVICE_TITLES = (
    "Manutenção de jardim residencial",
    "Reparo de vazamentos e torneiras",
    "Pintura interna de apartamento",
    "Limpeza residencial periódica",
    "Instalação de luminárias",
    "Pequenos reparos domésticos",
    "Configuração de computadores e redes",
    "Revisão mecânica preventiva",
    "Montagem de móveis residenciais",
    "Fotografia de eventos sociais",
    "Criação de identidade visual",
    "Reforma de ambientes internos",
    "Poda de árvores e arbustos",
    "Instalação de chuveiro e torneira",
    "Pintura externa de casa",
    "Limpeza pós-obra de apartamento",
    "Reparo de tomadas e interruptores",
    "Manutenção de portas e janelas",
    "Formatação e suporte para notebook",
    "Diagnóstico de falhas automotivas",
    "Instalação de prateleiras e suportes",
    "Ensaio fotográfico profissional",
    "Design de peças para redes sociais",
    "Assentamento de revestimentos",
    "Plantio e renovação de gramado",
    "Desentupimento de pias e ralos",
    "Preparação e pintura de paredes",
    "Higienização de estofados residenciais",
    "Instalação elétrica residencial",
    "Montagem de armários e estantes",
    "Recuperação de arquivos e computador",
    "Troca de óleo e filtros automotivos",
    "Montagem de móveis de escritório",
    "Fotografia de produtos para catálogo",
    "Criação de material gráfico para negócios",
    "Reparo de acabamento e alvenaria",
)
BANNERS = (
    (
        "demo-encontre-profissionais",
        "Encontre profissionais perto de você",
        "Explore serviços publicados por profissionais da sua região.",
        "Explorar serviços",
    ),
    (
        "demo-resolva-com-bico",
        "Resolva o que precisa com a BICO",
        "Descubra serviços para casa, trabalho e dia a dia.",
        "Buscar serviços",
    ),
    (
        "demo-talento-bico",
        "Seu talento tem espaço na BICO",
        "Conheça profissionais autônomos e empresas prestadoras.",
        "Conhecer a BICO",
    ),
)
CATEGORY_IMAGES = {
    "jardinagem": "garden-trimmer.webp",
    "encanamento": "plumbing-repair.webp",
    "pintura": "wall-painting.webp",
    "limpeza": "home-cleaning.webp",
    "eletrica": "electrical-installation.webp",
    "tecnologia": "computer-repair.webp",
    "mecanica": "automotive-diagnostics.webp",
    "fotografia": "event-photography.webp",
    "reformas": "wall-painting.webp",
}
PROVIDER_AVATARS = {
    "demo.provider01@example.invalid": "demo-provider-alex.webp",
    "demo.provider02@example.invalid": "demo-provider-beatriz.webp",
    "demo.provider03@example.invalid": "demo-provider-caio.webp",
}
DEMO_GARDEN_GALLERY = (
    ("lawn-mowing.webp", "Corte de grama em jardim residencial"),
    ("garden-hedge-pruning.webp", "Poda e manutenção de cerca viva"),
    ("garden-planting.webp", "Plantio e cuidado de jardim"),
)


class Command(BaseCommand):
    help = "Cria conteúdo demonstrativo idempotente para a Home BICO em MySQL local."

    def handle(self, *args, **options):
        if not settings.DEBUG or connection.vendor != "mysql":
            raise CommandError("O seed só pode ser executado com DEBUG=True e MySQL.")

        category_count, categories = self._seed_categories()
        providers = self._seed_providers(categories)
        listings = self._seed_listings(categories)
        banners = self._seed_banners()
        self.stdout.write(
            self.style.SUCCESS(
                "Seed BICO concluído sem sobrescrever registros existentes: "
                f"{category_count} categorias, {providers} perfis, "
                f"{listings} anúncios e {banners} banners."
            )
        )

    def _seed_categories(self):
        created_count = 0
        for order, (name, slug, featured, specialty) in enumerate(CATEGORIES, start=1):
            _category, created = ServiceCategory.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "display_order": order,
                    "is_active": True,
                    "is_featured": featured,
                    "is_specialty": specialty,
                },
            )
            created_count += int(created)
        categories = [
            ServiceCategory.objects.get(slug=slug)
            for _name, slug, _featured, _specialty in CATEGORIES
        ]
        for category in categories:
            if not category.cover_image and (filename := CATEGORY_IMAGES.get(category.slug)):
                self._attach_image_if_empty(category, "cover_image", filename)
        return created_count, categories

    def _seed_providers(self, categories):
        User = get_user_model()
        created_count = 0
        all_names = [(name, ProviderProfile.ProviderType.INDIVIDUAL) for name in INDIVIDUAL_NAMES]
        all_names.extend((name, ProviderProfile.ProviderType.COMPANY) for name in COMPANY_NAMES)
        city = "Campinas"

        for index, (name, provider_type) in enumerate(all_names, start=1):
            email = f"demo.provider{index:02d}@example.invalid"
            user, user_created = User.objects.get_or_create(
                email=email,
                defaults={"name": name},
            )
            if user_created:
                user.set_unusable_password()
                user.save(update_fields=["password"])
            else:
                existing_profile = ProviderProfile.objects.filter(user=user).first()
                if (
                    user.name != name
                    or existing_profile is None
                    or not existing_profile.is_demo
                    or existing_profile.public_name != name
                ):
                    self.stdout.write(f"Ignorado por conflito com conta existente: {email}")
                    continue

            profile, profile_created = ProviderProfile.objects.get_or_create(
                user=user,
                defaults={
                    "provider_type": provider_type,
                    "public_name": name,
                    "description": f"Perfil fictício de demonstração da BICO para {name}.",
                    "city": city,
                    "state": "SP",
                    "status": ProviderProfile.Status.APPROVED,
                    "approved_at": timezone.now(),
                    "is_featured": provider_type == ProviderProfile.ProviderType.INDIVIDUAL
                    and index <= 8,
                    "is_demo": True,
                },
            )
            if not profile_created and not profile.is_demo:
                self.stdout.write(f"Ignorado por conflito com perfil não demonstrativo: {name}")
                continue
            if profile.is_demo:
                profile.categories.add(categories[(index - 1) % len(categories)])
                if filename := PROVIDER_AVATARS.get(email):
                    self._attach_image_if_empty(profile, "avatar", filename)
            if profile_created:
                created_count += 1
        return created_count

    def _seed_listings(self, categories):
        created_count = 0
        eligible_providers = list(
            ProviderProfile.objects.filter(
                is_demo=True, status=ProviderProfile.Status.APPROVED
            ).order_by("public_name")
        )
        if not eligible_providers:
            return 0

        for index in range(36):
            provider = eligible_providers[index % len(eligible_providers)]
            category = categories[index % len(categories)]
            title = SERVICE_TITLES[index % len(SERVICE_TITLES)]
            slug = f"demo-servico-{index + 1:02d}"
            price_type = (
                ServiceListing.PriceType.FROM if index % 3 else ServiceListing.PriceType.QUOTE
            )
            description = (
                f"Anúncio fictício de demonstração. {title} oferecido por "
                f"{provider.public_name} em Campinas-SP."
            )
            listing, created = ServiceListing.objects.get_or_create(
                slug=slug,
                defaults={
                    "provider": provider,
                    "category": category,
                    "title": title,
                    "description": description,
                    "price_start": None
                    if price_type == ServiceListing.PriceType.QUOTE
                    else 90 + (index % 9) * 25,
                    "price_type": price_type,
                    "city": provider.city,
                    "state": provider.state,
                    "status": ServiceListing.Status.PUBLISHED,
                    "is_featured": index < 8,
                    "is_demo": True,
                    "published_at": timezone.now(),
                },
            )
            if (
                not created
                and listing.is_demo
                and (listing.title != title or listing.description != description)
            ):
                listing.title = title
                listing.description = description
                listing.save(update_fields=["title", "description", "updated_at"])
            if listing.is_demo:
                filename = CATEGORY_IMAGES.get(category.slug)
                if filename:
                    self._attach_image_if_empty(listing, "image", filename)
                if slug == "demo-servico-01":
                    self._seed_garden_gallery(listing)
            created_count += int(created)
        return created_count

    def _seed_garden_gallery(self, listing):
        if not listing.is_demo:
            return
        for order, (filename, alt_text) in enumerate(DEMO_GARDEN_GALLERY):
            image, _created = ServiceListingImage.objects.get_or_create(
                listing=listing,
                display_order=order,
                defaults={"alt_text": alt_text},
            )
            if not image.alt_text:
                image.alt_text = alt_text
                image.save(update_fields=["alt_text"])
            self._attach_image_if_empty(image, "image", filename)

    def _seed_banners(self):
        created_count = 0
        for order, (slug, title, subtitle, action) in enumerate(BANNERS, start=1):
            banner, created = HomeBanner.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "subtitle": subtitle,
                    "action_label": action,
                    "destination": "/servicos/",
                    "display_order": order,
                    "is_active": True,
                    "is_demo": True,
                },
            )
            if banner.is_demo and not banner.image:
                filename = {
                    "demo-encontre-profissionais": "garden-trimmer.webp",
                    "demo-resolva-com-bico": "computer-repair.webp",
                    "demo-talento-bico": "wall-painting.webp",
                }.get(slug)
                if filename:
                    self._attach_image_if_empty(banner, "image", filename)
                    banner.image_alt = f"Imagem demonstrativa: {title.lower()}"
                    banner.save(update_fields=["image_alt"])
            created_count += int(created)
        return created_count

    def _attach_image_if_empty(self, instance, field_name, filename):
        image_field = getattr(instance, field_name)
        if image_field:
            return False
        source = settings.BASE_DIR / "static" / "marketplace" / "demo" / filename
        if not source.is_file():
            self.stdout.write(self.style.WARNING(f"Asset demonstrativo ausente: {filename}"))
            return False
        image_field.save(filename, ContentFile(source.read_bytes()), save=True)
        return True
