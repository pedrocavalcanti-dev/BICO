# Marketplace público — serviços e perfis

## Descoberta e categorias

A Home e a busca permanecem públicas. A faixa do cabeçalho lista até sete categorias ativas com `is_featured=True`, ordenadas pelo catálogo, mais o link para todas. A seleção é administrada pelo Django Admin no registro da categoria; nomes não são codificados nos templates.

O catálogo público exige categoria ativa, prestador aprovado e anúncio publicado. O detalhe do anúncio usa o mesmo seletor da busca e oferece links para categoria e perfil. Serviço relacionado é limitado a quatro anúncios da mesma categoria.

## Galeria e conteúdo demonstrativo

`ServiceListingImage` relaciona imagens ao anúncio. Cada foto possui texto alternativo e posição única dentro do anúncio; o campo `ServiceListing.image` segue como capa compatível com anúncios anteriores. Se a capa estiver vazia, a primeira imagem ordenada da galeria assume a apresentação principal. Os serializers públicos retornam `image`, `alt_text` e `display_order`.

O diretório `bico_django/static/marketplace/demo/` contém imagens de origem geradas para demonstração e um mapa de uso. Desde a Alpha 0.3.1, `seed_bico_demo` copia arquivos apenas para registros demonstrativos de categoria, perfil, anúncio ou banner e não atualiza registros não demonstrativos. Imagens são encaminhadas a `MEDIA_ROOT` pelo `ImageField`. O storage definitivo de produção continua pendente.

Na Alpha 0.3.2, o manifesto foi ampliado com 81 assets WebP gerados para esta demonstração. O seed preenche imagens ausentes e substitui apenas nomes conhecidos das imagens demonstrativas antigas para corrigir placeholders. Ele também reconhece o sufixo aleatório de sete caracteres que o storage Django pode acrescentar a esses nomes, mantendo idempotência em execuções futuras. Arquivos personalizados são preservados. No MySQL local, os 36 anúncios publicados têm capas únicas e ao menos uma imagem de galeria distinta, as 12 categorias têm foto e os 18 perfis demonstrativos têm retrato ou logo. Execuções repetidas não criaram registros nem mudaram os nomes das imagens já semeadas.

O Django Admin exige duas imagens distintas ao criar um anúncio já publicado ou mudar um rascunho para publicado. Rascunhos podem permanecer sem fotos. Anúncios já publicados antes desta regra continuam editáveis. Futuros fluxos de publicação devem usar `ServiceListing.has_minimum_publication_images()`; a API pública segue apenas leitura e seu contrato de galeria não mudou.

## Detalhe de serviço

`/servicos/<slug>/` apresenta galeria, categoria, título, prestador, cidade/UF, preço quando definido, descrição e serviços relacionados. Avaliações mostram estado vazio porque ainda não há modelo de avaliações. A área de atendimento não presume raio ou distância.

“Solicitar serviço” e “Conversar com profissional” pedem login e retornam a uma página informativa. Não criam pedidos nem enviam mensagens; esses recursos pertencem a versões futuras.

## Perfil público

`/profissionais/<slug>/` mostra nome, tipo, cidade/UF, categorias ativas, apresentação, anúncios públicos e portfólio extraído das galerias dos próprios anúncios. Outros perfis são limitados a profissionais aprovados na mesma cidade e com categoria em comum. Não há nota, contagem de serviços, disponibilidade, status online ou selo de verificação sem fonte real.

O refinamento visual Alpha 0.3.2 apresenta os anúncios em cards mais largos, o portfólio em grade e profissionais relacionados em cards compactos com avatar/logo, especialidade e cidade. A empresa usa seu logo próprio; retratos e logos demonstrativos não representam pessoas ou marcas reais.

O detalhe `GET /api/v1/providers/{uuid}/` inclui até 12 anúncios públicos. Endpoints de lista e Home não expandem listagens por perfil. `GET /api/v1/listings/{uuid}/` e listas de anúncio incluem `gallery_images`. Todos permanecem somente leitura e sem campos de conta privada.

## Não incluído

Contratação, mensagens, favoritos, avaliações, pagamentos, mapa, geolocalização, login social e onboarding profissional não foram implementados nesta release.
