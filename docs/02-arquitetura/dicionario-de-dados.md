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

Perfis pessoais, profissionais, serviços, solicitações, conversas e avaliações ainda não possuem tabelas nesta fundação.
