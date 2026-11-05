# Estado atual

**Versão:** 0.3.0-alpha

**Atualizado:** 2026-11-05

**Ambiente inspecionado:** Windows, PowerShell, Python 3.12.10, Django 5.2.19, DRF 3.18.3, MySQL Server 8.0.46

## Alpha 0.3.0 — autenticação e área do cliente

- Conta única de cliente com cadastro por nome/e-mail/senha, hash Django e login imediato; confirmação de e-mail ainda não existe.
- Login/logout por sessão Django, logout POST/CSRF, retorno `next` restrito ao próprio host e política explícita de sessão persistente.
- Recuperação de senha pelos tokens temporários Django; mensagens em arquivo local durante desenvolvimento e SMTP exigido em produção.
- Minha Conta e edição restrita ao nome, mudança de senha com senha atual, formulários responsivos e menu compartilhado conforme a sessão.
- Throttle de login/cadastro/reset persistido em buckets HMAC no MySQL; eventos relevantes gravados em `audit` sem senha, token, IP ou payload pessoal.
- `GET/PATCH /api/v1/users/me/` opera apenas sobre `request.user`, exige autenticação e CSRF na mutação e permite editar somente o nome.
- Home permanece pública. Links de ações pessoais usam login; destinos legados de autenticação e conta redirecionam para as rotas novas.

## Alpha 0.2.0 — Home do marketplace

- Home de marketplace responsiva na ordem visual aprovada: header/busca, categorias, banners, profissionais, serviços em destaque, chamada para prestadores, área reservada a mapa, anúncios, empresas, novidades, especialidades e footer.
- Fontes locais Inter variável e Quicksand 700; tokens de pesos, famílias, tamanhos e cores atualizados para as referências tipográficas fornecidas.
- Apps `providers` e `catalog`; modelos `ProviderProfile`, `ServiceCategory`, `ServiceListing` e `HomeBanner`, com UUID, relações, estados de publicação, datas, índices e campos demonstrativos.
- Seletores compartilhados entre a Home/API, restringindo perfis a `APPROVED` e anúncios a `PUBLISHED` com categoria ativa.
- Busca Web por título, categoria, prestador e cidade; páginas simples de resultados, anúncio e perfil; destinos informativos para ações futuras.
- API v1 pública de leitura para Home, categorias, perfis e anúncios; paginação limitada e serializers sem dados privados.
- Admin técnico dos quatro modelos e comando MySQL/DEBUG `seed_bico_demo`, idempotente e sem remoção ou alteração de registros legítimos.
- Fallbacks CSS locais quando banners, capas, avatars ou imagens de anúncio não estão disponíveis. Nenhuma imagem externa é carregada.
- Área de proximidade sem mapa, geolocalização, distância ou pins falsos.

## Validação da Alpha 0.2.0

- `manage.py check`: sem erros.
- `makemigrations --check --dry-run`: nenhuma migration pendente após gerar as migrations versionadas.
- `manage.py migrate --noinput`: aplicou apenas as novas tabelas e índices `catalog`, `providers` e `core` no MySQL local existente; não criou nem apagou o schema.
- `manage.py test`: 21 testes passaram. São testes unitários/web/API sem criação de banco temporário.
- Seed inicial criou 12 categorias, 18 perfis demonstrativos, 36 anúncios e 3 banners. Reexecuções não criaram duplicatas; os 36 títulos demonstrativos são distintos.
- Cliente Django contra o banco local: `/`, `/servicos/`, busca filtrada, endpoints raiz/health/Home/categorias/perfis/anúncios responderam 200.
- Testes confirmaram `POST`, `PUT`, `DELETE` e `OPTIONS` recusados em listagens públicas e parâmetros de busca fora do limite retornando 400.
- `findstatic` localizou `css/home.css`, `js/home.js` e a fonte Inter vendorizada.
- Página inteira conferida no Edge em 360, 390, 768, 1024 e 1440 px, sem overflow horizontal do documento; capturas locais estão em `artifacts/responsive-alpha-0.2.0/` e são ignoradas pelo Git.

## Validação da Alpha 0.3.0

- `manage.py check`: sem erros.
- `makemigrations --check --dry-run`: nenhuma migration pendente.
- Migration `accounts.0002_auththrottlebucket`: consta aplicada no MySQL local.
- `manage.py test`: a suíte completa encontrou 40 testes, mas parou antes de executá-los porque `bico_app` não tem permissão para criar `test_bico` (MySQL 1044). Em separado, 20 testes sem acesso ao banco passaram (`UserModelContractTests` e `apps.core.tests`).
- Ruff `check` e `format --check` nos arquivos Python alterados: sem erros.
- Login e cadastro conferidos no Edge em 360, 390, 768, 1024 e 1440 px, sem overflow horizontal; capturas locais em `artifacts/responsive-alpha-0.3.0/` são ignoradas pelo Git.

## Histórico Git e integração

- A Alpha 0.2.0 está no commit `3702e69`; a Alpha 0.3.0 parte dele e está no commit `dba6100`, na branch `feature/bico-alpha-0.3.0-auth`.
- A publicação desta branch de desenvolvimento está autorizada. A integração à `main` fica pendente até a suíte completa executar e passar no MySQL de teste; preservar a ordem Alpha 0.2.0 → Alpha 0.3.0.

## Regras e limites

- O estado aprovado de perfil e publicado de anúncio controla a descoberta pública. E-mail, usuário, estado de moderação e dados documentais não fazem parte dos serializers públicos.
- Conteúdo demonstrativo tem `is_demo=True`, senha inutilizável e identificação visual na Home. Ele existe apenas no MySQL de desenvolvimento; o comando falha fora de `DEBUG=True` e MySQL.
- Não há avaliações, preço presumido, distância, localização precisa ou status de verificação inventados. Anúncios demonstrativos podem mostrar preço ou “Sob orçamento” porque isso está explicitamente marcado como demonstração.
- Confirmação de e-mail, ativação de prestador, solicitação/contratação, chat, notificações funcionais, favoritos persistentes, avaliações, mapa real e pagamentos permanecem pendentes.
- Fotos e banners oficiais ainda não foram recebidos; a interface usa fallback CSS até existirem imagens autorizadas. O Figma editável não está no repositório, então a composição segue as referências visuais compartilhadas.

## Próximos passos

Implementar habilitação de perfil profissional com regras de aprovação; depois, solicitações de serviços. Planejar confirmação de e-mail, armazenamento definitivo de mídia e mapa somente com requisitos e dados adequados.
