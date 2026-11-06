# Marketplace público — serviços e perfis

## Descoberta e categorias

A Home e a busca permanecem públicas. A faixa do cabeçalho lista até sete categorias ativas com `is_featured=True`, ordenadas pelo catálogo, mais o link para todas. A seleção é administrada pelo Django Admin no registro da categoria; nomes não são codificados nos templates.

O catálogo público exige categoria ativa, prestador aprovado e anúncio publicado. O detalhe do anúncio usa o mesmo seletor da busca e oferece links para categoria e perfil. Serviço relacionado é limitado a quatro anúncios da mesma categoria.

## Galeria e conteúdo demonstrativo

`ServiceListingImage` relaciona imagens ao anúncio. Cada foto possui texto alternativo e posição única dentro do anúncio; o campo `ServiceListing.image` segue como capa compatível com anúncios anteriores. Se a capa estiver vazia, a primeira imagem ordenada da galeria assume a apresentação principal. Os serializers públicos retornam `image`, `alt_text` e `display_order`.

O diretório `bico_django/static/marketplace/demo/` contém imagens de origem geradas para demonstração e um mapa de uso. `seed_bico_demo` copia arquivos somente se o campo ainda estiver vazio e o perfil/anúncio/banner for demonstrativo; não substitui imagens preenchidas nem atualiza registros não demonstrativos. Imagens são encaminhadas a `MEDIA_ROOT` pelo `ImageField`. O storage definitivo de produção continua pendente.

## Detalhe de serviço

`/servicos/<slug>/` apresenta galeria, categoria, título, prestador, cidade/UF, preço quando definido, descrição e serviços relacionados. Avaliações mostram estado vazio porque ainda não há modelo de avaliações. A área de atendimento não presume raio ou distância.

“Solicitar serviço” e “Conversar com profissional” pedem login e retornam a uma página informativa. Não criam pedidos nem enviam mensagens; esses recursos pertencem a versões futuras.

## Perfil público

`/profissionais/<slug>/` mostra nome, tipo, cidade/UF, categorias ativas, apresentação, anúncios públicos e portfólio extraído das galerias dos próprios anúncios. Outros perfis são limitados a profissionais aprovados na mesma cidade e com categoria em comum. Não há nota, contagem de serviços, disponibilidade, status online ou selo de verificação sem fonte real.

O detalhe `GET /api/v1/providers/{uuid}/` inclui até 12 anúncios públicos. Endpoints de lista e Home não expandem listagens por perfil. `GET /api/v1/listings/{uuid}/` e listas de anúncio incluem `gallery_images`. Todos permanecem somente leitura e sem campos de conta privada.

## Não incluído

Contratação, mensagens, favoritos, avaliações, pagamentos, mapa, geolocalização, login social e onboarding profissional não foram implementados nesta release.
