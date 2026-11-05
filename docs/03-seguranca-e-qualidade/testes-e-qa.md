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
