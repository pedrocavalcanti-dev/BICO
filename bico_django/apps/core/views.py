import re

from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from apps.catalog.models import ServiceCategory
from apps.providers.models import ProviderProfile

from .selectors import active_categories, home_sections, public_listings, search_listings

INFO_PAGES = {
    "entrar": (
        "Entrar na BICO",
        "A entrada de clientes e prestadores estará disponível em uma próxima etapa.",
    ),
    "criar-conta": ("Criar conta", "O cadastro de clientes e prestadores está em desenvolvimento."),
    "minha-conta": (
        "Minha conta",
        "As ferramentas da conta estarão disponíveis após a etapa de autenticação.",
    ),
    "conversar": ("Conversas", "O chat entre clientes e prestadores ainda não está disponível."),
    "notificacoes": (
        "Notificações",
        "As notificações serão disponibilizadas em uma próxima etapa.",
    ),
    "quem-somos": (
        "Sobre a BICO",
        "A BICO conecta pessoas a profissionais e empresas que prestam serviços.",
    ),
    "como-funciona": (
        "Como funciona",
        "A descoberta pública de serviços já está disponível. "
        "Solicitações e contratação serão implementadas depois.",
    ),
    "seguranca": (
        "Segurança",
        "Os perfis e anúncios públicos são exibidos conforme seu estado de publicação. "
        "Recursos adicionais serão documentados quando implementados.",
    ),
    "termos": (
        "Termos de uso",
        "Os termos públicos estão em preparação e serão publicados "
        "antes da abertura para usuários reais.",
    ),
    "privacidade": (
        "Privacidade",
        "A política pública de privacidade está em preparação. "
        "Esta versão não solicita localização precisa.",
    ),
    "ajuda": ("Central de ajuda", "A central de ajuda será publicada em uma próxima etapa."),
    "suporte": (
        "Suporte",
        "O canal de suporte ainda não está disponível. "
        "Não há telefone ou endereço comercial publicado nesta versão.",
    ),
    "perguntas-frequentes": (
        "Perguntas frequentes",
        "As perguntas frequentes serão publicadas quando os fluxos "
        "de contratação estiverem disponíveis.",
    ),
    "para-prestadores": (
        "Para prestadores",
        "Profissionais e empresas poderão criar perfis e divulgar serviços "
        "após a etapa de cadastro.",
    ),
    "regras-da-comunidade": (
        "Regras da comunidade",
        "As regras serão publicadas antes do lançamento dos fluxos de interação.",
    ),
    "contato": ("Contato", "Um canal de contato público será informado quando estiver disponível."),
    "redes-sociais": (
        "Redes sociais",
        "Os canais oficiais da BICO serão publicados nesta página quando definidos.",
    ),
}


def home(request):
    sections = home_sections()
    sections["navigation_categories"] = active_categories()[:10]
    sections["banners"] = list(sections["banners"])
    if not sections["banners"]:
        sections["banners"] = [
            {
                "title": "Encontre profissionais perto de você",
                "subtitle": (
                    "Descubra serviços para cuidar da casa, do trabalho e do seu dia a dia."
                ),
                "action_label": "Explorar serviços",
                "destination": "/servicos/",
                "image": None,
                "mobile_image": None,
                "image_alt": "",
                "is_demo": False,
            }
        ]
    return render(
        request,
        "public/home.html",
        sections,
    )


def search(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("categoria", "").strip().lower()
    city = request.GET.get("cidade", "").strip()
    if len(query) > 100 or len(city) > 100 or len(category) > 150:
        return HttpResponseBadRequest("Use até 100 caracteres para busca e cidade.")
    if category and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", category):
        return HttpResponseBadRequest("A categoria informada é inválida.")

    results = search_listings(query=query, category=category, city=city)
    paginator = Paginator(results, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "public/search_results.html",
        {
            "page_obj": page_obj,
            "query": query,
            "city": city,
            "selected_category": category,
            "categories": active_categories(),
            "navigation_categories": active_categories()[:10],
            "result_count": paginator.count,
        },
    )


def listing_detail(request, slug):
    listing = get_object_or_404(public_listings().select_related("provider", "category"), slug=slug)
    return render(
        request,
        "public/service_detail.html",
        {"listing": listing, "navigation_categories": active_categories()[:10]},
    )


def provider_detail(request, slug):
    provider = get_object_or_404(
        ProviderProfile.objects.filter(status=ProviderProfile.Status.APPROVED)
        .select_related("user")
        .prefetch_related(
            Prefetch("categories", queryset=ServiceCategory.objects.filter(is_active=True))
        ),
        slug=slug,
    )
    listings = public_listings().filter(provider=provider).order_by("-published_at")[:12]
    return render(
        request,
        "public/provider_detail.html",
        {
            "provider": provider,
            "listings": listings,
            "navigation_categories": active_categories()[:10],
        },
    )


def info_page(request, slug):
    account_destinations = {
        "entrar": "accounts:login",
        "criar-conta": "accounts:register",
        "minha-conta": "accounts:account",
        "conversar": "accounts:conversations",
        "notificacoes": "accounts:notifications",
    }
    if destination := account_destinations.get(slug):
        return redirect(destination)

    page = INFO_PAGES.get(slug)
    if page is None:
        raise Http404
    return render(
        request,
        "public/info_page.html",
        {
            "title": page[0],
            "message": page[1],
            "navigation_categories": active_categories()[:10],
        },
    )
