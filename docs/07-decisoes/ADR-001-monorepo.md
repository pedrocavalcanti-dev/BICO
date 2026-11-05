# ADR-001 — Monorepositório

- **Estado:** aceito.
- **Contexto:** equipe pequena desenvolve backend, web e posteriormente mobile/gestão.
- **Decisão:** manter um repositório com Django em `bico_django/`, documentação em `docs/` e espaço futuro para `mobile/`.
- **Consequência:** mudanças relacionadas são revisáveis juntas; limites de diretório e ownership de domínio evitam acoplamento.
