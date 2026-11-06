import re

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
    "manutencao-residencial": "listing-06-cover.webp",
    "tecnologia": "computer-repair.webp",
    "mecanica": "automotive-diagnostics.webp",
    "montagem-de-moveis": "listing-09-cover.webp",
    "fotografia": "event-photography.webp",
    "design": "listing-11-cover.webp",
    "reformas": "sheet-12-1.webp",
}
PROVIDER_AVATARS = {
    "demo.provider01@example.invalid": "demo-provider-alex.webp",
    "demo.provider02@example.invalid": "demo-provider-beatriz.webp",
    "demo.provider03@example.invalid": "demo-provider-caio.webp",
    **{
        f"demo.provider{index:02d}@example.invalid": f"demo-provider-{index:02d}.webp"
        for index in range(4, 16)
    },
}
COMPANY_LOGOS = {
    "demo.provider16@example.invalid": "demo-company-equipe-verde.webp",
    "demo.provider17@example.invalid": "demo-company-casa-em-ordem.webp",
    "demo.provider18@example.invalid": "demo-company-oficina-horizonte.webp",
}
PROFILE_SPECIALTIES = {
    "demo.provider01@example.invalid": ("jardinagem",),
    "demo.provider02@example.invalid": ("encanamento",),
    "demo.provider03@example.invalid": ("mecanica",),
    "demo.provider04@example.invalid": ("pintura",),
    "demo.provider05@example.invalid": ("eletrica",),
    "demo.provider06@example.invalid": ("limpeza",),
    "demo.provider07@example.invalid": ("tecnologia",),
    "demo.provider08@example.invalid": ("fotografia",),
    "demo.provider09@example.invalid": ("montagem-de-moveis",),
    "demo.provider10@example.invalid": ("design",),
    "demo.provider11@example.invalid": ("reformas",),
    "demo.provider12@example.invalid": ("manutencao-residencial",),
    "demo.provider13@example.invalid": ("pintura", "encanamento"),
    "demo.provider14@example.invalid": ("limpeza",),
    "demo.provider15@example.invalid": ("eletrica",),
    "demo.provider16@example.invalid": ("jardinagem",),
    "demo.provider17@example.invalid": ("limpeza",),
    "demo.provider18@example.invalid": ("mecanica",),
}
PROFILE_PRESENTATIONS = {
    "demo.provider01@example.invalid": (
        "Cuido de jardins residenciais com corte de grama, poda leve e plantio, "
        "combinando o escopo conforme cada espaço."
    ),
    "demo.provider02@example.invalid": (
        "Realizo instalações e reparos hidráulicos em torneiras, chuveiros e ralos de residências."
    ),
    "demo.provider03@example.invalid": (
        "Atuo com revisão preventiva e diagnóstico mecânico de automóveis em Campinas."
    ),
    "demo.provider04@example.invalid": (
        "Faço pintura interna e externa, com preparação cuidadosa das superfícies "
        "antes da aplicação."
    ),
    "demo.provider05@example.invalid": (
        "Atendo instalações elétricas residenciais, luminárias, tomadas e interruptores."
    ),
    "demo.provider06@example.invalid": (
        "Ofereço limpeza residencial periódica e organização básica de ambientes."
    ),
    "demo.provider07@example.invalid": (
        "Presto suporte para computadores, notebooks e redes domésticas."
    ),
    "demo.provider08@example.invalid": (
        "Fotografo eventos, retratos e produtos para pessoas e pequenos negócios."
    ),
    "demo.provider09@example.invalid": (
        "Monto móveis residenciais e de escritório, seguindo as especificações de cada peça."
    ),
    "demo.provider10@example.invalid": (
        "Crio peças gráficas e materiais visuais para comunicação de pequenos negócios."
    ),
    "demo.provider11@example.invalid": (
        "Realizo reformas e acabamentos internos, com escopo definido após avaliação do ambiente."
    ),
    "demo.provider12@example.invalid": (
        "Faço pequenos reparos residenciais em portas, janelas e acabamentos."
    ),
    "demo.provider13@example.invalid": (
        "Atendo serviços de pintura e reparos hidráulicos residenciais em Campinas."
    ),
    "demo.provider14@example.invalid": (
        "Trabalho com limpeza pós-obra e higienização de estofados residenciais."
    ),
    "demo.provider15@example.invalid": "Realizo reparos e instalações elétricas em residências.",
    "demo.provider16@example.invalid": (
        "A Equipe Verde cuida de jardins residenciais, gramados, podas e plantios."
    ),
    "demo.provider17@example.invalid": (
        "A Casa em Ordem oferece limpeza periódica e pós-obra para residências."
    ),
    "demo.provider18@example.invalid": (
        "A Oficina Horizonte atende revisões preventivas e reparos mecânicos automotivos."
    ),
}
LISTING_PROVIDER_EMAILS = (
    "demo.provider01@example.invalid",
    "demo.provider02@example.invalid",
    "demo.provider04@example.invalid",
    "demo.provider06@example.invalid",
    "demo.provider05@example.invalid",
    "demo.provider12@example.invalid",
    "demo.provider07@example.invalid",
    "demo.provider03@example.invalid",
    "demo.provider09@example.invalid",
    "demo.provider08@example.invalid",
    "demo.provider10@example.invalid",
    "demo.provider11@example.invalid",
    "demo.provider16@example.invalid",
    "demo.provider02@example.invalid",
    "demo.provider13@example.invalid",
    "demo.provider17@example.invalid",
    "demo.provider15@example.invalid",
    "demo.provider12@example.invalid",
    "demo.provider07@example.invalid",
    "demo.provider18@example.invalid",
    "demo.provider09@example.invalid",
    "demo.provider08@example.invalid",
    "demo.provider10@example.invalid",
    "demo.provider11@example.invalid",
    "demo.provider01@example.invalid",
    "demo.provider13@example.invalid",
    "demo.provider04@example.invalid",
    "demo.provider14@example.invalid",
    "demo.provider05@example.invalid",
    "demo.provider12@example.invalid",
    "demo.provider07@example.invalid",
    "demo.provider03@example.invalid",
    "demo.provider09@example.invalid",
    "demo.provider08@example.invalid",
    "demo.provider10@example.invalid",
    "demo.provider11@example.invalid",
)
DEMO_GARDEN_GALLERY = (
    ("lawn-mowing.webp", "Corte de grama em jardim residencial"),
    ("garden-hedge-pruning.webp", "Poda e manutenção de cerca viva"),
    ("garden-planting.webp", "Plantio e cuidado de jardim"),
)
LISTING_COVERS = {
    1: "garden-trimmer.webp",
    2: "plumbing-repair.webp",
    3: "wall-painting.webp",
    4: "home-cleaning.webp",
    5: "electrical-installation.webp",
    6: "listing-06-cover.webp",
    7: "computer-repair.webp",
    8: "automotive-diagnostics.webp",
    9: "listing-09-cover.webp",
    10: "event-photography.webp",
    11: "listing-11-cover.webp",
    12: "sheet-12-1.webp",
    13: "sheet-01-1.webp",
    14: "sheet-02-1.webp",
    15: "sheet-03-1.webp",
    16: "sheet-04-1.webp",
    17: "sheet-05-1.webp",
    18: "sheet-06-1.webp",
    19: "sheet-07-1.webp",
    20: "sheet-08-1.webp",
    21: "sheet-09-1.webp",
    22: "sheet-10-1.webp",
    23: "sheet-11-1.webp",
    24: "sheet-12-3.webp",
    25: "sheet-01-3.webp",
    26: "sheet-02-3.webp",
    27: "sheet-03-3.webp",
    28: "sheet-04-3.webp",
    29: "sheet-05-3.webp",
    30: "sheet-06-3.webp",
    31: "sheet-07-3.webp",
    32: "sheet-08-3.webp",
    33: "sheet-09-3.webp",
    34: "sheet-10-3.webp",
    35: "sheet-11-3.webp",
    36: "sheet-13-1.webp",
}
LISTING_GALLERIES = {
    1: tuple(filename for filename, _alt in DEMO_GARDEN_GALLERY),
    2: ("sheet-14-1.webp",),
    3: ("sheet-14-2.webp",),
    4: ("sheet-14-3.webp",),
    5: ("sheet-14-4.webp",),
    6: ("listing-06-gallery.webp",),
    7: ("sheet-15-1.webp",),
    8: ("sheet-15-2.webp", "sheet-15-4.webp"),
    9: ("listing-09-gallery.webp",),
    10: ("sheet-15-3.webp",),
    11: ("listing-11-gallery.webp",),
    12: ("sheet-12-2.webp",),
    13: ("sheet-01-2.webp",),
    14: ("sheet-02-2.webp",),
    15: ("sheet-03-2.webp",),
    16: ("sheet-04-2.webp",),
    17: ("sheet-05-2.webp",),
    18: ("sheet-06-2.webp",),
    19: ("sheet-07-2.webp",),
    20: ("sheet-08-2.webp",),
    21: ("sheet-09-2.webp",),
    22: ("sheet-10-2.webp",),
    23: ("sheet-11-2.webp",),
    24: ("sheet-12-4.webp",),
    25: ("sheet-01-4.webp",),
    26: ("sheet-02-4.webp",),
    27: ("sheet-03-4.webp",),
    28: ("sheet-04-4.webp",),
    29: ("sheet-05-4.webp",),
    30: ("sheet-06-4.webp",),
    31: ("sheet-07-4.webp",),
    32: ("sheet-08-4.webp",),
    33: ("sheet-09-4.webp",),
    34: ("sheet-10-4.webp",),
    35: ("sheet-11-4.webp",),
    36: ("sheet-13-2.webp", "sheet-13-3.webp", "sheet-13-4.webp"),
}
SERVICE_DESCRIPTIONS = {
    "jardinagem": (
        "Cuidado de jardins residenciais, incluindo corte de grama, poda leve e "
        "plantio conforme as características do espaço."
    ),
    "encanamento": (
        "Instalações e reparos hidráulicos em torneiras, chuveiros e ralos, com "
        "escopo combinado após avaliação do local."
    ),
    "pintura": (
        "Pintura residencial com preparação das superfícies, proteção do ambiente e "
        "definição das etapas antes do início."
    ),
    "limpeza": (
        "Limpeza residencial periódica ou pós-obra, com atenção aos ambientes e às "
        "necessidades combinadas com o cliente."
    ),
    "eletrica": (
        "Instalações e reparos elétricos residenciais em luminárias, tomadas e interruptores."
    ),
    "manutencao-residencial": (
        "Pequenos reparos residenciais em portas, janelas, prateleiras e acabamentos."
    ),
    "tecnologia": (
        "Configuração, manutenção e suporte de computadores, notebooks e redes domésticas."
    ),
    "mecanica": (
        "Revisão preventiva e diagnóstico mecânico de automóveis. O escopo depende "
        "da avaliação do veículo."
    ),
    "montagem-de-moveis": (
        "Montagem de móveis residenciais e de escritório conforme as instruções e "
        "dimensões da peça."
    ),
    "fotografia": "Fotografia de eventos, retratos e produtos com planejamento de horário e local.",
    "design": (
        "Criação de peças gráficas e materiais visuais para comunicação de pessoas "
        "e pequenos negócios."
    ),
    "reformas": (
        "Serviços de reforma e acabamento interno com escopo definido após avaliação do ambiente."
    ),
}
REPLACEABLE_DEMO_IMAGES = {
    "garden-trimmer.webp",
    "lawn-mowing.webp",
    "garden-hedge-pruning.webp",
    "garden-planting.webp",
    "plumbing-repair.webp",
    "wall-painting.webp",
    "home-cleaning.webp",
    "electrical-installation.webp",
    "computer-repair.webp",
    "automotive-diagnostics.webp",
    "event-photography.webp",
}


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
            if filename := CATEGORY_IMAGES.get(category.slug):
                self._attach_seed_image(category, "cover_image", filename)
        return created_count, categories

    def _seed_providers(self, categories):
        User = get_user_model()
        created_count = 0
        categories_by_slug = {category.slug: category for category in categories}
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
                    "description": PROFILE_PRESENTATIONS[email],
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
                profile.categories.set(
                    [
                        categories_by_slug[slug]
                        for slug in PROFILE_SPECIALTIES[email]
                        if slug in categories_by_slug
                    ]
                )
                if profile.description.startswith("Perfil fictício de demonstração da BICO para"):
                    profile.description = PROFILE_PRESENTATIONS[email]
                    profile.save(update_fields=["description", "updated_at"])
                filename = COMPANY_LOGOS.get(email) or PROVIDER_AVATARS.get(email)
                if filename:
                    self._attach_seed_image(profile, "avatar", filename)
            if profile_created:
                created_count += 1
        return created_count

    def _seed_listings(self, categories):
        created_count = 0
        providers_by_email = {
            profile.user.email: profile
            for profile in ProviderProfile.objects.filter(
                is_demo=True, status=ProviderProfile.Status.APPROVED
            ).select_related("user")
        }
        categories_by_slug = {category.slug: category for category in categories}

        for index, title in enumerate(SERVICE_TITLES, start=1):
            provider = providers_by_email.get(LISTING_PROVIDER_EMAILS[index - 1])
            if provider is None:
                continue
            category_slug = CATEGORIES[(index - 1) % len(CATEGORIES)][1]
            category = categories_by_slug[category_slug]
            slug = f"demo-servico-{index:02d}"
            price_type = (
                ServiceListing.PriceType.FROM if index % 3 else ServiceListing.PriceType.QUOTE
            )
            description = SERVICE_DESCRIPTIONS[category.slug]
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
                    "is_featured": index <= 8,
                    "is_demo": True,
                    "published_at": timezone.now(),
                },
            )
            if listing.is_demo:
                update_fields = []
                if listing.title != title:
                    listing.title = title
                    update_fields.append("title")
                if listing.category_id != category.pk:
                    listing.category = category
                    update_fields.append("category")
                if listing.provider_id != provider.pk:
                    listing.provider = provider
                    listing.city = provider.city
                    listing.state = provider.state
                    update_fields.extend(["provider", "city", "state"])
                if listing.description.startswith("Anúncio fictício de demonstração."):
                    listing.description = description
                    update_fields.append("description")
                if update_fields:
                    listing.save(update_fields=[*update_fields, "updated_at"])

                self._attach_seed_image(listing, "image", LISTING_COVERS[index])
                gallery_filenames = LISTING_GALLERIES[index]
                gallery_alt_texts = self._gallery_alt_texts(title, gallery_filenames)
                self._seed_listing_gallery(
                    listing,
                    tuple(zip(gallery_filenames, gallery_alt_texts, strict=True)),
                )
            created_count += int(created)
        return created_count

    def _gallery_alt_texts(self, title, filenames):
        if title == SERVICE_TITLES[0]:
            return tuple(alt for _filename, alt in DEMO_GARDEN_GALLERY)
        descriptions = (
            "fotografia principal do trabalho",
            "detalhe complementar do serviço",
            "outra etapa do serviço",
        )
        return tuple(f"{title} — {description}" for description in descriptions[: len(filenames)])

    def _seed_listing_gallery(self, listing, photos):
        if not listing.is_demo:
            return
        for order, (filename, alt_text) in enumerate(photos):
            image, _created = ServiceListingImage.objects.get_or_create(
                listing=listing,
                display_order=order,
                defaults={"alt_text": alt_text},
            )
            if not image.alt_text:
                image.alt_text = alt_text
                image.save(update_fields=["alt_text"])
            self._attach_seed_image(image, "image", filename)

    def _attach_seed_image(self, instance, field_name, filename):
        image_field = getattr(instance, field_name)
        current_filename = image_field.name.rsplit("/", 1)[-1] if image_field else ""
        if current_filename == filename or self._matches_storage_name(current_filename, filename):
            return False
        is_replaceable_legacy = any(
            self._matches_storage_name(current_filename, known_name)
            for known_name in REPLACEABLE_DEMO_IMAGES
        )
        if image_field and not is_replaceable_legacy:
            return False
        source = settings.BASE_DIR / "static" / "marketplace" / "demo" / filename
        if not source.is_file():
            self.stdout.write(self.style.WARNING(f"Asset demonstrativo ausente: {filename}"))
            return False
        image_field.save(filename, ContentFile(source.read_bytes()), save=True)
        return True

    def _matches_storage_name(self, current_filename, expected_filename):
        stem, extension = expected_filename.rsplit(".", 1)
        collision_pattern = rf"{re.escape(stem)}_[A-Za-z0-9]{{7}}\.{re.escape(extension)}"
        return current_filename == expected_filename or bool(
            re.fullmatch(collision_pattern, current_filename)
        )

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
