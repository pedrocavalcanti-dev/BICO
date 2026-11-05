# ADR-003 — PostgreSQL

- **Estado:** aceito.
- **Contexto:** marketplace requer integridade relacional e evolução para consultas geográficas.
- **Decisão:** PostgreSQL é o banco local/principal; sem fallback SQLite; PostGIS será avaliado quando houver necessidade.
- **Consequência:** ambiente de desenvolvimento precisa de PostgreSQL antes de aplicar migrations ou executar testes integrados.
