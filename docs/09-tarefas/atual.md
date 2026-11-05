# Tarefa atual — Alpha 0.3.0: autenticação e área do cliente

- [x] Inspecionar estado Git, `AGENTS.md`, arquitetura, User, segurança, URLs, templates e API da Alpha 0.2.0.
- [x] Criar `feature/bico-alpha-0.3.0-auth` a partir do commit da Home `3702e69`.
- [x] Implementar conta única, validação de senha, login, sessão persistente opcional e logout POST/CSRF.
- [x] Implementar recuperação nativa Django, resposta neutra, e-mail de desenvolvimento em arquivo e SMTP obrigatório em produção.
- [x] Implementar Minha Conta, edição allowlist de nome e mudança de senha autenticada.
- [x] Integrar header compartilhado e proteger ações pessoais; preservar a Home pública.
- [x] Implementar `GET/PATCH /api/v1/users/me/` com sessão, CSRF, serializer allowlist e usuário derivado da sessão.
- [x] Implementar throttle MySQL com chaves HMAC e auditoria sem credenciais/PII.
- [x] Criar migration não destrutiva e comando de limpeza de buckets antigos.
- [x] Atualizar documentação funcional, interface, API, segurança, release e ADR mobile futuro.
- [x] `manage.py check`, `makemigrations --check --dry-run`, Ruff `check`/`format --check` e `git diff --check` passaram.
- [ ] Suíte Django completa: encontrou 40 testes, mas não conseguiu iniciar porque `bico_app` não tem privilégio para criar `test_bico` (MySQL 1044). Aguardando o privilégio no banco de teste.
- [x] 20 testes sem acesso ao banco passaram (`UserModelContractTests` e `apps.core.tests`).
- [x] Revisar login e cadastro no Edge em 360, 390, 768, 1024 e 1440 px; confirmar ausência de overflow horizontal.
- [x] Revisar diff final e registrar o commit local `feat: implement BICO authentication and customer account`.

Dependência: esta branch deriva de `feature/bico-alpha-0.2.0-home` no commit `3702e69`; integrar a Home antes desta branch. Pendências do produto: confirmação de e-mail, MFA, login social, modo Prestador, chat, favoritos, notificações reais e contratação. Não realizar push remoto.
