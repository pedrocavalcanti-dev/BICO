# Testes e QA

Checks iniciais previstos:

```powershell
Set-Location .\bico_django
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py check --deploy --settings=config.settings.production
python manage.py findstatic css/site.css
```

Migrations aplicadas, criação de superuser e testes que dependam do banco requerem MySQL acessível com permissões adequadas. A ausência de credenciais ou do serviço deve ser registrada como bloqueio, sem trocar silenciosamente por PostgreSQL ou SQLite. Os resultados da execução atual estão em `01-projeto/estado-atual.md`.

O runner padrão do Django cria e remove o banco temporário `test_bico`. No ambiente local, `bico_app` não pode criá-lo e a suíte completa para antes de executar os casos (erro MySQL 1044). MySQL aceita privilégios no nível do banco, incluindo `CREATE` e `DROP`; concedê-los no padrão escapado do banco de teste não os estende a outros bancos. Um administrador pode executar:

```sql
GRANT ALL PRIVILEGES ON `test\_bico`.* TO 'bico_app'@'127.0.0.1';
SHOW GRANTS FOR 'bico_app'@'127.0.0.1';
```

O escape de `_` evita tratá-lo como curinga no padrão de privilégios. Essa concessão inclui permissões de criação/remoção somente no banco `test_bico`; não concede privilégios em `bico` ou `*.*`. Ela ainda não foi executada nesta sessão porque não há conexão administrativa MySQL disponível. Após a concessão, executar `python manage.py test` em `bico_django/` e confirmar que os testes foram executados. Nunca apontar o runner para o banco principal `Bico`/`bico` como atalho. Em 2026-11-05, `manage.py check`, `makemigrations --check --dry-run`, 22 testes focados de `apps.core.tests`, Ruff nos Python alterados e `git diff --check` passaram; a suíte completa permaneceu bloqueada antes de executar os testes.
