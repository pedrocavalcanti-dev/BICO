# Dicionário de dados — fundação

## `accounts_user`

| Campo | Tipo/uso |
|---|---|
| `id` | UUID, chave primária |
| `email` | E-mail único e identificador de login; normalizado em minúsculas |
| `name` | Nome de exibição inicial |
| `password` | Hash gerenciado pelo Django; nunca armazenar senha em texto |
| `is_active`, `is_staff`, `is_superuser` | Estado e acesso técnico do Django |
| `groups`, `user_permissions` | Permissões Django via `PermissionsMixin` |
| `created_at`, `updated_at`, `last_login` | Datas de ciclo de vida e autenticação |

## `audit_auditevent`

UUID, ator opcional (`SET_NULL`), ação, tipo/identificador do alvo, resultado, metadados JSON mínimos e data de criação. Não é um log de payloads: conteúdo de mensagens, senhas, tokens e dados pessoais não devem ser gravados.

## `accounts_auththrottlebucket`

Chave HMAC primária, início de janela e contador para limitar tentativas de autenticação em múltiplos processos usando o MySQL compartilhado. Não armazena IP ou e-mail em claro. Buckets antigos são removidos pelo comando `cleanup_auth_throttle`.

## `providers_providerprofile`

Perfil público 1:1 com usuário, tipo `INDIVIDUAL`/`COMPANY`, nome público, slug, descrição, avatar opcional, cidade/UF, categorias, estado de aprovação, destaque, marca demonstrativa e datas. Não contém CPF/CNPJ, e-mail público nem endereço preciso.

## `catalog_servicecategory`

Nome e slug únicos, descrição, capa e referência de ícone opcionais, ordem, ativo, destaque, especialidade e datas.

## `catalog_servicelisting`

Anúncio UUID com prestador e categoria, título/slug, descrição, imagem opcional, preço inicial Decimal opcional, tipo `FROM`/`QUOTE`, cidade/UF pública, estado `DRAFT`/`PUBLISHED`/`PAUSED`/`ARCHIVED`, destaque, marca demonstrativa e datas de criação/publicação/atualização.

## `core_homebanner`

Título, subtítulo, imagens desktop/mobile opcionais, texto alternativo, rótulo e destino interno, ordem, ativo, marca demonstrativa e datas. O destino validado é sempre um caminho interno.

## `catalog_servicelistingimage`

Galeria 1:N de `catalog_servicelisting`: imagem validada, texto alternativo obrigatório, ordem e data de criação. A ordem é única dentro do mesmo anúncio. A migration `catalog.0003_servicelistingimage` somente cria a tabela e não altera os anúncios existentes.

Avaliações, solicitações, pagamentos, conversas e localização geográfica ainda não possuem tabelas nesta versão.
