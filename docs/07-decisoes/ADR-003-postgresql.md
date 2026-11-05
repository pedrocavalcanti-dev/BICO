# ADR-003 — PostgreSQL

- **Estado:** substituído por [ADR-006 — MySQL](ADR-006-mysql.md).
- **Contexto:** marketplace requer integridade relacional e evolução para consultas geográficas.
- **Decisão histórica:** PostgreSQL foi escolhido inicialmente para desenvolvimento e produção, sem fallback SQLite; PostGIS seria avaliado quando houvesse necessidade.
- **Consequência histórica:** a configuração PostgreSQL nunca foi validada com o servidor local na Alpha 0.1.0. A decisão vigente é MySQL, registrada no ADR-006.
