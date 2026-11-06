# Estado atual

**Versão em desenvolvimento:** 0.3.2-alpha
**Atualizado:** 2026-11-05
**Branch:** `feature/bico-alpha-0.3.2-visual-assets`
**Commit da implementação:** `e857cbb` (publicado em `origin/feature/bico-alpha-0.3.2-visual-assets`)
**Ambiente:** Windows, PowerShell, Python 3.12.10, Django 5.2.19, DRF 3.18.3, MySQL Server 8.0.46

## Alpha 0.3.2 — imagens e refinamento visual

- O seed demonstrativo agora distribui 81 novos arquivos WebP locais: 60 fotografias de trabalho em recortes distintos, seis imagens avulsas, 12 retratos e três logos originais de empresas fictícias. Os arquivos novos somam aproximadamente 4,1 MiB; a origem está registrada em `bico_django/static/marketplace/demo/README.md`.
- No MySQL local, os 36 anúncios demonstrativos publicados têm capa e ao menos uma foto adicional com nome de arquivo distinto (41 fotos de galeria no total); nenhum nome de capa se repete entre anúncios demonstrativos.
- As 12 categorias têm imagem; os 18 perfis demonstrativos têm retrato ou logo próprio. O seed corrige somente relacionamentos e imagens de registros `is_demo=True`, além das imagens de categoria identificadas como placeholders antigos. Imagens personalizadas e registros reais são preservados.
- O seed completa apresentações e especialidades dos perfis e associa cada anúncio demonstrativo a um profissional coerente. Execuções repetidas não criam novas imagens nem duplicam registros.
- O detalhe de anúncio mantém a galeria acessível da Alpha 0.3.1 com conteúdo demonstrativo completo. O perfil profissional foi reorganizado em cabeçalho mais compacto, cards de serviços com largura útil, portfólio visual e perfis relacionados apresentados em cards. Logos de empresas usam recorte próprio sem deformação; as trilhas horizontais da Home ocultam a barra apenas em desktop, mantendo a rolagem.
- O Django Admin impede publicar novos anúncios sem duas imagens distintas entre capa e galeria. Rascunhos continuam permitidos sem imagens; anúncios já publicados antes da regra seguem editáveis. A função de domínio também está disponível para um futuro fluxo de publicação. Não houve alteração de schema ou migration.

## Validação da Alpha 0.3.2

- `manage.py check` passou; `manage.py makemigrations --check --dry-run` informou que não há migrations pendentes.
- 28 testes focados de `apps.catalog.tests` e `apps.core.tests` passaram sem usar o banco de testes.
- Ruff passou nos quatro módulos Python alterados (`admin.py`, `models.py`, `seed_bico_demo.py` e `tests.py`); `git diff --check` também passou.
- O seed foi executado repetidamente no MySQL local com `DEBUG=True` sem criar registros ou trocar os nomes de arquivos já associados. Consulta confirmou 36 capas únicas, 41 imagens de galeria, 12 categorias com imagem e 18 perfis demonstrativos com retrato/logo.
- Os 81 novos assets foram verificados como imagens WebP legíveis, com hashes distintos e tamanho individual inferior a 500 KB. A inspeção em navegador com viewport de 412 px e 1440 px confirmou Home, anúncio e perfil sem rolagem horizontal da página.
- `git diff --check` passou. A suíte completa permanece bloqueada antes da execução porque o usuário MySQL local não pode criar `test_bico` (erro 1044); não foi usado o schema principal para contornar isso. Nenhuma migration ou alteração de API foi necessária.

## Alpha 0.3.1 — Marketplace Experience Update

- Navegação do cabeçalho usa até sete categorias ativas e destacadas do MySQL, selecionáveis pelo campo `is_featured` no admin, mais o destino “Todas as categorias”. Em telas estreitas, a rolagem fica contida na navegação.
- Página pública de anúncio ganhou galeria de capa/miniaturas acessível, resumo do serviço, prestador, cidade/UF, preço quando configurado, descrição, estado vazio de avaliações e serviços relacionados. Ações de solicitação e conversa explicam que não criam pedido nem enviam mensagem; visitantes seguem para login.
- Perfil público apresenta identidade, especialidades, descrição, anúncios publicados, portfólio formado pelas galerias de anúncios, estado vazio de avaliações e profissionais aprovados da mesma cidade/categoria. Não exibe estatísticas, distância, nota, disponibilidade ou verificação sem dados reais.
- `ServiceListingImage` adiciona imagens relacionadas com texto alternativo, ordem e restrição única por anúncio/ordem. A migration `catalog.0003_servicelistingimage` é não destrutiva e aparece aplicada no banco MySQL local (`showmigrations`).
- Serializer público de anúncio inclui `gallery_images`; detalhe de prestador inclui até 12 anúncios públicos. O serializer usado em listas/home não expande anúncios por prestador, evitando consultas N+1. Os filtros públicos existentes continuam exigindo perfil aprovado, anúncio publicado e categoria ativa.
- O seed `seed_bico_demo` copia assets locais para registros demonstrativos de categoria, perfil, anúncio e banner. Pode preencher campos vazios ou substituir nomes de placeholders antigos explicitamente permitidos, incluindo o sufixo aleatório de sete caracteres do storage; mídia personalizada e registros não demonstrativos permanecem intactos.
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

`feature/bico-alpha-0.3.1-experience` deriva de `feature/bico-alpha-0.3.0-auth`, commit `0be5a3e`, e foi publicada em `origin` no commit `c116678`. A Alpha 0.3.0 deriva da Home no commit `3702e69`. A `main` local está em `e1a2cdd`; `origin` ainda não publica uma branch `main`. Não integrar esta branch antes da suíte integral passar e da revisão visual final.
