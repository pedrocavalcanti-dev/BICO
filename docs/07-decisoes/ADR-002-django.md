# ADR-002 — Django como backend

- **Estado:** aceito.
- **Contexto:** a BICO precisa de autenticação, admin técnico, templates e API reutilizável por uma equipe pequena.
- **Decisão:** usar Django 5.2 LTS, DRF e monólito modular; evitar microsserviços nesta etapa.
- **Consequência:** regras de negócio e permissões ficam centralizadas; domínios evoluem como apps dentro do mesmo backend.
