# Contratos API

Prefixo oficial: `/api/v1/`. Nesta etapa existem somente:

| Método | Rota | Resposta |
|---|---|---|
| GET | `/api/v1/` | `{"name":"BICO API","version":"v1"}` |
| GET | `/api/v1/health/` | `{"status":"ok"}` — liveness, sem revelar dependências |

Planejamento futuro: `auth`, `users`, `providers`, `categories`, `services`, `search`, `locations`, `service-requests`, `conversations`, `reviews`, `reports` e `notifications`. Não criar esses endpoints antes de existirem regras e contratos reais.
