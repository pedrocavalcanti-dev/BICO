# Banco de dados

MySQL 8.0.11 ou superior é obrigatório para desenvolvimento integrado e produção. A configuração usa `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` e `DB_PORT`, carregadas do ambiente e do `.env` na raiz do monorepo. `DB_ENGINE` deve ser `mysql`; configurações de outros backends são rejeitadas.

O driver único é `mysqlclient`. A conexão solicita `utf8mb4`, modo SQL estrito, isolamento `READ COMMITTED` e InnoDB para tabelas criadas pela conexão. Essas opções são por conexão/sessão; não alteram configurações globais do servidor. O banco existente deve usar `utf8mb4` e InnoDB; inspecione charset, collation, engines, tabelas e privilégios antes de migrar.

Não existe fallback para PostgreSQL ou SQLite. As credenciais locais não são versionadas. Produção exige usuário de aplicação com privilégios mínimos; não usar root.

Usuários e eventos de auditoria usam UUID. Chaves estrangeiras, constraints e migrations versionadas preservam integridade. PostGIS fica para quando houver necessidade operacional de busca geográfica.
