# Arquitetura

## Direção

Monólito modular Django, com limites de domínio claros. Django Templates atende a Web inicial; DRF oferece API REST para Web/PWA e futuros clientes móveis. Regras críticas devem residir no backend e ser reutilizáveis entre interfaces.

PostgreSQL é o banco principal. Não há fallback para SQLite. Não introduzir microsserviços, framework JavaScript ou infraestrutura externa sem necessidade e decisão registrada.

## Componentes existentes

- `config.settings`: base, desenvolvimento e produção.
- `apps.core`: Home pública.
- `apps.accounts`: identidade e usuário customizado.
- `apps.audit`: registro mínimo de eventos.
- `api.v1`: raiz e health check.

Outros domínios estão documentados, mas ainda não existem no código.
