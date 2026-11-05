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
- [ ] Suíte Django completa: encontrou 40 testes, mas não conseguiu iniciar porque `bico_app` não tem privilégio para criar `test_bico` (MySQL 1044). Reexecutar após configurar usuário de teste com permissões necessárias para criar/remover o banco isolado.
- [x] 20 testes sem acesso ao banco passaram (`UserModelContractTests` e `apps.core.tests`).
- [x] Revisar login e cadastro no Edge em 360, 390, 768, 1024 e 1440 px; confirmar ausência de overflow horizontal.
- [x] Revisar diff final e registrar o commit `dba6100 feat: implement BICO authentication and customer account`.
- [x] Publicar `feature/bico-alpha-0.3.0-auth` em `origin` sem force push.
- [ ] Integrar à `main` somente após a suíte completa executar e passar no MySQL de teste.

Dependência: `feature/bico-alpha-0.3.0-auth` deriva de `feature/bico-alpha-0.2.0-home` no commit `3702e69`; o commit de autenticação é `dba6100`. A Alpha 0.2.0 deve preceder esta versão na integração. Pendências do produto: confirmação de e-mail, MFA, login social, modo Prestador, chat, favoritos, notificações reais e contratação. A integração à `main` só deve ocorrer após a suíte completa passar; não usar push forçado.
