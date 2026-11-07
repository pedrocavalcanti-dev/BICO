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

## Onboarding do prestador — Alpha 0.4.0

| Método | Rota | Autenticação | Contrato |
|---|---|---|---|
| GET | `/api/v1/providers/onboarding/` | Sessão Django | Consulta a solicitação do usuário autenticado; campos de decisão, revisor e documentos são omitidos |
| PATCH | `/api/v1/providers/onboarding/` | Sessão Django + CSRF | Recebe `step` (1–4) e campos permitidos pela etapa; valida com os mesmos Django Forms da Web |
| POST | `/api/v1/providers/onboarding/documents/` | Sessão Django + CSRF, multipart | Recebe `side` (`FRONT` ou `BACK`) e `file`; valida, reprocessa e substitui o lado informado |
| POST | `/api/v1/providers/onboarding/submit/` | Sessão Django + CSRF | Valida completude/documentos e envia para revisão humana |

Os endpoints estão sujeitos à configuração de disponibilidade; em produção a implementação os deixa indisponíveis até aprovação jurídica e operacional. O usuário e a solicitação derivam de `request.user`, nunca de UUID fornecido pelo cliente. Upload e envio têm limites compartilhados por IP/usuário no MySQL. Imagens cifradas e respectivos caminhos não são retornados pela API; a prévia Web é privada, sem cache e limitada ao proprietário. Erros retornam validação DRF sem dados do arquivo. Envio repetido de uma solicitação já pendente é idempotente.

Campos CPF/CNPJ, dados de empresa, representante, endereço fixo e decisão/revisor não fazem parte das APIs públicas. A futura autenticação móvel continua documentada em ADR-008; estes endpoints usam sessão Web e não implementam JWT ou tokens mobile.

### Uso pela interface Alpha 0.4.1

Os endpoints e os payloads principais permanecem disponíveis. A interface usa PATCH para salvamento automático de etapas completas e válidas; requisições são serializadas para evitar sobrescrita por uma versão anterior. Uploads multipart usam o endpoint documental já existente durante a identificação, antes da revisão. Enviar a solicitação continua exigindo frente/verso válidos no serviço de domínio.

Os forms compartilhados exigem tipo PF/PJ, nome/apresentação/categoria principal e cidade/UF. A categoria principal é limitada ao mesmo conjunto ativo de especialidades. CEP informado é normalizado e validado em oito dígitos. Quando `fixed_point_city`/`fixed_point_state` não são fornecidos, usam `city`/`state`; nome do ponto vazio usa o nome profissional. Campos anteriores de endereço próprio continuam aceitos pela API. Não há endpoint de busca de CEP no backend; a consulta opcional é feita pelo navegador conforme ADR-011.

A ciência `acknowledged` pertence ao formulário Web final, sem alteração no contrato de submissão da API. Não é tratada como registro de aceite jurídico. Nenhum campo de aprovação, decisão ou revisor passou a ser editável.

## Área do Prestador — Alpha 0.4.1

| Método | Rota | Autenticação | Contrato |
|---|---|---|---|
| GET | `/api/v1/providers/me/dashboard/` | Sessão Django | Identidade pública, contagens reais de anúncios publicados/rascunhos/pausados e `views: null`, `views_available: false` |
| GET | `/api/v1/providers/me/profile/` | Sessão Django | Perfil profissional próprio: id, nome público, descrição, cidade/UF e especialidades |
| PATCH | `/api/v1/providers/me/profile/` | Sessão Django + CSRF | Atualiza somente nome público, descrição e especialidades ativas; id e cidade/UF são somente leitura |

Os endpoints exigem `ProviderProfile.status=APPROVED`; autorização usa o usuário da sessão, não um identificador recebido. Perfil/serializers não aceitam status, usuário, documento, aprovação, permissões ou dados de identidade. Alterações registram auditoria mínima. Ainda não existem endpoints para listagem/CRUD de anúncios, portfólio, área de atendimento ou autenticação mobile; as páginas Web permanecem no Django Templates.
