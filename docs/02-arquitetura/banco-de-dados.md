# Banco de dados

PostgreSQL é obrigatório para desenvolvimento integrado e produção. A configuração usa as variáveis `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST` e `POSTGRES_PORT`, carregadas do ambiente e do `.env` localizado na raiz do monorepo.

Não existe fallback SQLite. A ausência de PostgreSQL bloqueia migrações aplicadas e validações dependentes do banco, mas não deve impedir checks estáticos ou a geração de migrations quando possível.

Usuários e eventos de auditoria usam UUID. Chaves estrangeiras, constraints e migrations versionadas preservam integridade. PostGIS fica para quando houver necessidade operacional de busca geográfica.
