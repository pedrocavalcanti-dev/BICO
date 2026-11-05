# Estado atual

**Versão:** 0.1.0-alpha

**Atualizado:** 2026-11-04

**Ambiente inspecionado:** Windows, PowerShell, Python 3.12.10, Git 2.55.0

## Implementado

- Monorepositório e configuração Django dentro de `bico_django/`.
- Settings separados para base, desenvolvimento e produção.
- Apps `core`, `accounts` e `audit`; usuário UUID com e-mail de login.
- Migrations iniciais de `accounts` e `audit` geradas e revisadas.
- API v1 com raiz e health check públicos.
- Home pública simples com identidade laranja e CSS estático.
- `.gitignore`, `.env.example`, README, AGENTS e documentação inicial.

## Validado

- Django 5.2.19, DRF 3.18.3, django-environ 0.14.0 e psycopg 3.3.8 instalados no `.venv`.
- `manage.py check` sem problemas; `makemigrations --check --dry-run` sem mudanças (com aviso de histórico não verificável sem banco); sete testes sem banco passaram; CSS encontrado e coleta estática em dry-run concluída.
- `check --deploy` foi executado com variáveis temporárias e apontou somente HSTS desligado; mantido assim até domínio/TLS/proxy serem definidos.
- O `runserver` não iniciou porque o Django consulta o histórico de migrations no boot; PostgreSQL/`psql` estão ausentes e `127.0.0.1:5432` recusou conexão.

## Pendências

- Aplicar migrations e validar criação de superuser após PostgreSQL estar disponível.
- Reexecutar validação integrada com PostgreSQL e verificação de produção ao configurar o ambiente final.
- Definir provedor de hospedagem e estratégia de deploy.

## Próxima etapa

Disponibilizar PostgreSQL, criar banco/usuário `bico` (ou atualizar `.env`), concluir as validações da fundação e então iniciar Alpha 0.2.0: cadastro, login, logout, recuperação de senha e perfil pessoal.
