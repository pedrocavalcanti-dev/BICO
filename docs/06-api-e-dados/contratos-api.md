# Contratos API

Prefixo oficial: `/api/v1/`. As rotas de descoberta são públicas, somente leitura e declaram `AllowAny` sem autenticação por sessão/token. `GET` e `HEAD` são os únicos métodos habilitados. Listas paginam por `page` e aceitam `page_size` limitado a 48.

| Método | Rota | Parâmetros | Resposta |
|---|---|---|---|
| GET | `/api/v1/home/` | — | Seções limitadas de banners, profissionais, categorias, anúncios e empresas |
| GET | `/api/v1/categories/` | `featured=true/false`, `page`, `page_size` | Categorias ativas |
| GET | `/api/v1/providers/` | `q`, `category`, `city`, `type`, `page`, `page_size` | Perfis aprovados |
| GET | `/api/v1/providers/{uuid}/` | — | Perfil aprovado |
| GET | `/api/v1/listings/` | `q`, `category`, `city`, `page`, `page_size` | Anúncios publicados de perfis aprovados e categorias ativas |
| GET | `/api/v1/listings/{uuid}/` | — | Anúncio publicável |
| GET | `/api/v1/` | — | Metadados da API v1 |
| GET | `/api/v1/health/` | — | `{"status":"ok"}` — liveness |

Busca aceita até 100 caracteres para texto/cidade e 150 para slug de categoria; tipo de perfil deve ser `INDIVIDUAL` ou `COMPANY`. Erros de parâmetro retornam 400. As consultas da Web e API compartilham os seletores de `catalog`, `providers` e `core`.

Os serializers públicos não incluem e-mail, usuário relacionado, estado administrativo ou dados documentais. O campo `is_demo` permite identificar conteúdo demonstrativo. Anúncios incluem `gallery_images` como lista de `{image, alt_text, display_order}`; URLs representam imagens públicas associadas ao anúncio.

O detalhe `/api/v1/providers/{uuid}/` inclui `listings` (no máximo 12), serializados com a mesma regra de publicação e galeria. Listagens de provedores e seções da Home usam o serializer compacto sem expandir anúncios por perfil, para limitar consultas.

Formato de listagem DRF: `count`, `next`, `previous`, `results`. Não existe escrita pública para estes recursos.

## Endpoints anteriores

Planejamento futuro: autenticação/cadastro, solicitações, mensagens, avaliações, notificações e localização geográfica. Eles não fazem parte das rotas implementadas.

## Conta autenticada — Alpha 0.3.0

| Método | Rota | Autenticação | Resposta |
|---|---|---|---|
| GET | `/api/v1/users/me/` | Sessão Django | `name`, `email`, `created_at` do usuário da sessão |
| PATCH | `/api/v1/users/me/` | Sessão Django + CSRF | Atualiza somente `name`; e-mail e data são somente leitura |

O endpoint deriva o objeto exclusivamente de `request.user`. Não recebe UUID de usuário, ignora campos adicionais e não expõe flags/permissões. A sessão Web usa `SessionAuthentication`; mutações exigem token CSRF. Não há endpoints API de login, cadastro ou tokens mobile nesta versão.
