# ADR-009 — Galerias de anúncio e mídia demonstrativa local

- **Status:** Aceita para Alpha 0.3.1
- **Data:** 2026-11-05

## Contexto

O detalhe de serviço precisa de várias imagens, e o protótipo precisa de imagens coerentes sem dependência de URLs externas instáveis. O modelo de anúncio tem uma capa opcional; o Django já valida e armazena uploads com `ImageField`.

## Decisão

- Manter `ServiceListing.image` como capa retrocompatível e adicionar `ServiceListingImage` como relação 1:N ordenada, com texto alternativo e unicidade de ordem por anúncio.
- Versionar assets gerados apenas como origem de conteúdo demonstrativo em `static/marketplace/demo/`. O comando `seed_bico_demo`, em MySQL e `DEBUG=True`, copia esses arquivos para o storage configurado de imagens, somente em campos vazios e entidades demonstrativas.
- Não tratar `static/` como storage de uploads de usuários. Seleção do backend de produção, política de retenção e otimização de uploads reais continuam para uma decisão futura.
- Expor galerias em serializers públicos de anúncio e anúncios no detalhe do perfil, reutilizando os seletores públicos e limitando a expansão a 12 anúncios.

## Consequências

Os dados locais usam a mesma abstração de `ImageField` que as páginas e APIs usam para mídia. O seed é idempotente e não troca mídia já preenchida. Conteúdo demonstrativo é sinalizado no produto e não representa pessoas, serviços, verificação ou avaliação reais. A migration adiciona apenas nova tabela e pode ser aplicada sem alterar linhas de anúncios existentes.

## Alternativas consideradas

- Depender de imagens externas: descartado por instabilidade, disponibilidade e direitos de uso incertos.
- Repetir a capa como várias fotos: descartado porque não cria uma galeria verdadeira e piora a demonstração.
- Salvar uploads diretamente em `static/`: descartado por misturar conteúdo editável com assets versionados e não servir como storage de usuário.
