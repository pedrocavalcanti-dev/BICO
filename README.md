# BICO — Plataforma de Serviços

Fundação técnica `0.1.0-alpha` de um marketplace bilateral para descoberta e contratação de serviços, iniciado em Campinas-SP. A conta é única: uma pessoa poderá contratar e, opcionalmente, ativar um perfil profissional.

Esta etapa entrega a base Django, a API versionada, a Home pública mínima e a documentação de arquitetura. Catálogo, contratação, chat, pagamentos e BICO Gestão ainda não estão implementados. O Alpha atual é exclusivamente de serviços; não inclui comércio de produtos.

## Estrutura

- `bico_django/`: projeto Django, apps, API, templates e arquivos estáticos.
- `docs/`: decisões, escopo, arquitetura, segurança e estado real do produto.
- `mobile/`: reservado para o futuro aplicativo Flutter; ainda não iniciado.

## Requisitos

- Python 3.12 ou 3.13.
- PostgreSQL 14 ou superior, com banco e usuário criados localmente.
- PowerShell no Windows.

Dependências Python estão fixadas em `requirements.txt`. Django 5.2 é a linha LTS e o DRF é configurado para exigir autenticação por padrão nas futuras rotas protegidas. Consulte [docs/indice.md](docs/indice.md) antes de alterar arquitetura.

## Preparar o ambiente local

Na raiz do repositório:

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -c "from pathlib import Path; import secrets; p=Path('.env'); p.write_text(p.read_text(encoding='utf-8').replace('replace-with-a-random-secret-key', secrets.token_urlsafe(64)), encoding='utf-8')"
```

Preencha as variáveis `POSTGRES_*` conforme o PostgreSQL local. O projeto não troca para SQLite se o PostgreSQL estiver indisponível.

Depois que o banco existir:

```powershell
Set-Location .\bico_django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

A aplicação fica em `http://127.0.0.1:8000/`; a API em `/api/v1/` e o health check em `/api/v1/health/`.

## Settings

- Desenvolvimento: `config.settings.development` (padrão do `manage.py`).
- Produção: `config.settings.production`; exige secret, credenciais PostgreSQL, hosts permitidos e origens CSRF explícitas.

O `.env` é carregado a partir da raiz do monorepo, independentemente do diretório atual do terminal. Não versionar `.env`, credenciais, uploads privados ou dados reais.

## Validar

Com as dependências instaladas:

```powershell
Set-Location .\bico_django
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py findstatic css/site.css
```

`migrate` e testes que usam banco precisam de PostgreSQL disponível. Consulte [docs/01-projeto/estado-atual.md](docs/01-projeto/estado-atual.md) para os resultados da inicialização deste ambiente.

## Git

O bootstrap cria um commit local em `main`. A publicação é manual e exige revisar o destino remoto antes de executar `git push`; nenhum push é realizado automaticamente.
