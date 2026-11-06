# Estado atual

**Versão em desenvolvimento:** 0.3.1-alpha
**Atualizado:** 2026-11-05
**Branch:** `feature/bico-alpha-0.3.1-experience`
**Ambiente:** Windows, PowerShell, Python 3.12.10, Django 5.2.19, DRF 3.18.3, MySQL Server 8.0.46

## Alpha 0.3.1 — Marketplace Experience Update

- Navegação do cabeçalho usa até sete categorias ativas e destacadas do MySQL, selecionáveis pelo campo `is_featured` no admin, mais o destino “Todas as categorias”. Em telas estreitas, a rolagem fica contida na navegação.
- Página pública de anúncio ganhou galeria de capa/miniaturas acessível, resumo do serviço, prestador, cidade/UF, preço quando configurado, descrição, estado vazio de avaliações e serviços relacionados. Ações de solicitação e conversa explicam que não criam pedido nem enviam mensagem; visitantes seguem para login.
- Perfil público apresenta identidade, especialidades, descrição, anúncios publicados, portfólio formado pelas galerias de anúncios, estado vazio de avaliações e profissionais aprovados da mesma cidade/categoria. Não exibe estatísticas, distância, nota, disponibilidade ou verificação sem dados reais.
- `ServiceListingImage` adiciona imagens relacionadas com texto alternativo, ordem e restrição única por anúncio/ordem. A migration `catalog.0003_servicelistingimage` é não destrutiva e aparece aplicada no banco MySQL local (`showmigrations`).
- Serializer público de anúncio inclui `gallery_images`; detalhe de prestador inclui até 12 anúncios públicos. O serializer usado em listas/home não expande anúncios por prestador, evitando consultas N+1. Os filtros públicos existentes continuam exigindo perfil aprovado, anúncio publicado e categoria ativa.
- O seed `seed_bico_demo` foi ampliado de forma idempotente para copiar assets locais somente para campos vazios de categorias, perfis/anúncios demonstrativos e banners demonstrativos. Galeria do anúncio demonstrativo de jardinagem usa três imagens adicionais. Registros não demonstrativos e imagens já existentes não são alterados.
- Há imagens WebP geradas para demonstração, com mapa de uso em `bico_django/static/marketplace/demo/README.md`. Não são pessoas, serviços, avaliações nem recomendações reais. O seed copia os arquivos para `MEDIA_ROOT`; `static/` não é storage de uploads de usuários.
- Login mostra o ícone oficial Google com botão desabilitado e estado “Em breve”; autenticação social não está integrada. A origem e o limite de uso estão em `static/branding/logos/README.md`.

## Validação da Alpha 0.3.1

- `manage.py check`: passou sem problemas.
- `manage.py makemigrations catalog --noinput`: gerou `0003_servicelistingimage`.
- `manage.py makemigrations --check --dry-run`: nenhuma alteração de migration pendente.
- Testes sem acesso a banco em `apps.core.tests`: 22 testes passaram, incluindo contrato de galeria/API, proteção do endpoint de ação anônima e validação da migration/modelo.
- Ruff `check` e `format --check` passaram nos arquivos Python alterados pela Alpha 0.3.1; `git diff --check` passou.
- `seed_bico_demo` foi executado duas vezes sem criar registros duplicados. Consulta local confirmou imagens para nove categorias, três avatares demonstrativos, 27 capas de anúncios, três imagens de galeria e três banners.
- Cliente Django recebeu HTTP 200 na Home, em detalhe de anúncio e perfil, e nos endpoints públicos de anúncio e prestador. A API do anúncio retornou três imagens de galeria; a API do perfil incluiu os anúncios relacionados. O servidor local serviu CSS, JavaScript e mídia com HTTP 200.
- Ruff `check`/`format --check` passou nos dez arquivos Python alterados. Uma varredura mais ampla ainda encontra 29 violações de estilo em arquivos preexistentes não alterados (`apps/accounts/admin.py` e migrations iniciais de accounts/catalog/core).
- `manage.py test --verbosity 1` encontrou 45 testes, mas parou antes da execução ao criar o banco MySQL isolado: a conta `bico_app` não tem privilégio para `test_bico` (erro 1044). Nenhum teste foi executado contra o banco principal para contornar esse bloqueio.
- A inspeção visual nos breakpoints 360, 390, 768, 1024 e 1440 px segue pendente. A tentativa de captura com Edge reutilizou a sessão já aberta e não gerou screenshots; por isso, não se declara validação visual desta versão.

## Alpha 0.3.0 — autenticação e área do cliente

- Cadastro, login/logout por sessão Django, recuperação e troca de senha, Minha Conta e edição allowlist do nome.
- `GET/PATCH /api/v1/users/me/` deriva o usuário da sessão e limita o PATCH ao nome.
- Throttle MySQL com chaves HMAC, auditoria sem credenciais/PII excessiva e redirecionamento `next` restrito.
- Em validação anterior, `check`, checagem de migrations, Ruff e 20 testes sem banco passaram. A suíte completa parou antes dos testes pelo erro 1044 de criação de `test_bico`.

## Alpha 0.2.0 — marketplace público

- Home, navegação, busca pública, categorias, perfis, anúncios e banners a partir de modelos MySQL; API v1 pública de leitura; seed demonstrativo.
- Conteúdo público exige perfil aprovado, anúncio publicado e categoria ativa. A Home foi validada anteriormente em Edge em 360, 390, 768, 1024 e 1440 px; 21 testes sem banco passaram.
- Commit da Home: `3702e69`, ancestral das branches de autenticação e experiência.

## Limites e pendências

- Solicitações, contratação, chat, favoritos persistentes, notificações reais, avaliações, modo Prestador, login Google, mapa, pagamentos e aplicativos continuam não implementados.
- Confirmação de e-mail não está disponível. Não há avaliações, notas, distância ou estado online/verificado reais nos perfis demonstrativos.
- Antes de integrar a versão à `main`, provisionar o banco de teste MySQL isolado e executar a suíte completa. Não conceder privilégio global ao usuário da aplicação e não rodar testes no schema principal `Bico`.
- Fazer revisão visual das páginas de anúncio/perfil em 360, 390, 768, 1024 e 1440 px quando houver uma sessão de navegador independente disponível.

## Histórico Git

`feature/bico-alpha-0.3.1-experience` deriva de `feature/bico-alpha-0.3.0-auth`, commit `0be5a3e`. A Alpha 0.3.0 deriva da Home no commit `3702e69`. A `main` local ainda está em `e1a2cdd`; não integrar esta branch antes da suíte integral passar e de confirmar o estado remoto.
