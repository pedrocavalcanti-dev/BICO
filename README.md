# BICO — Plataforma de Serviços

Alpha `0.3.1` da BICO: marketplace público com cadastro, login por sessão, área do cliente, galeria de anúncios e perfis públicos aprimorados. A conta é única; a ativação de prestador, confirmação de e-mail, contratação, chat, avaliações e pagamentos ainda não estão implementados.

Esta versão preserva a Home, busca, páginas públicas e APIs de leitura da Alpha 0.2.0; inclui recuperação de senha, edição segura do nome, sessão Web, `GET/PATCH /api/v1/users/me/`, detalhe público com galeria e perfil profissional com portfólio demonstrativo. O marketplace continua exclusivamente de serviços; não inclui comércio de produtos físicos.

## Estrutura

- `bico_django/`: projeto Django, apps, API, templates e arquivos estáticos.
- `docs/`: decisões, escopo, arquitetura, segurança e estado real do produto.
- `mobile/`: reservado para o futuro aplicativo Flutter; ainda não iniciado.

## Requisitos

- Python 3.12 ou 3.13.
- MySQL 8.0.11 ou superior, com o banco `Bico` já criado e usuário de conexão configurado.
- PowerShell no Windows.

Dependências Python estão fixadas em `requirements.txt`. Django 5.2 é a linha LTS e o DRF é configurado para exigir autenticação por padrão nas futuras rotas protegidas. Consulte [docs/indice.md](docs/indice.md) antes de alterar arquitetura.

## Preparar o ambiente local

Na raiz do repositório:

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
python -c "from pathlib import Path; import secrets; p=Path('.env'); p.write_text(p.read_text(encoding='utf-8').replace('replace-with-a-random-secret-key', secrets.token_urlsafe(64)), encoding='utf-8')"
```

Preencha `DB_USER` e `DB_PASSWORD` no `.env` com as credenciais locais autorizadas. `DB_NAME=Bico`, host e porta já indicam o banco existente. O projeto não cria nem recria o schema automaticamente e não troca para outro banco se o MySQL estiver indisponível.

Em desenvolvimento, a recuperação de senha grava mensagens em `bico_django/.local-emails/`; não envia e-mail externo. Em produção, configure `EMAIL_HOST`, `EMAIL_FROM` e as credenciais SMTP no ambiente antes de iniciar a aplicação. Nunca coloque segredos no Git.

Depois que o banco existir, aplique as migrations e inicie a aplicação:

```powershell
Set-Location .\bico_django
python manage.py migrate
python manage.py seed_bico_demo
python manage.py createsuperuser
python manage.py runserver
```

`seed_bico_demo` só executa com `DEBUG=True` e MySQL. Ele cria conteúdo fictício identificável como demonstração e copia imagens WebP locais para campos vazios; não apaga conteúdo nem substitui mídia já existente. Os assets e seu mapa estão em `bico_django/static/marketplace/demo/README.md`. Fotos demonstrativas não representam pessoas ou serviços reais. O storage para uploads em produção ainda precisa ser definido.

A aplicação fica em `http://127.0.0.1:8000/`; a API em `/api/v1/` e o health check em `/api/v1/health/`.

## Settings

- Desenvolvimento: `config.settings.development` (padrão do `manage.py`).
- Produção: `config.settings.production`; exige secret, credenciais MySQL, hosts permitidos e origens CSRF explícitas. Use uma conta MySQL de aplicação com privilégios mínimos, nunca `root`.

O `.env` é carregado a partir da raiz do monorepo, independentemente do diretório atual do terminal. Não versionar `.env`, credenciais, uploads privados ou dados reais.

## Validar

Com as dependências instaladas:

```powershell
Set-Location .\bico_django
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py findstatic css/site.css
python manage.py findstatic css/home.css
```

`migrate` e testes que usam banco precisam de MySQL disponível e credenciais válidas. Consulte [docs/01-projeto/estado-atual.md](docs/01-projeto/estado-atual.md) para o resultado da validação neste ambiente.

O runner de testes MySQL cria um banco isolado (`test_bico`). Use uma conta de teste autorizada a criar e remover esse banco; não conceda esses privilégios à conta de aplicação de produção. Sem isso, os testes focados que não precisam de banco podem passar, mas a suíte completa não chega a executar.

O CSS usa tokens, fontes locais Inter e Quicksand, base, componentes reutilizáveis e estilos específicos em `home.css`, `accounts/auth.css` e `marketplace/detail.css`. Consulte [estado atual](docs/01-projeto/estado-atual.md), [contratos da API](docs/06-api-e-dados/contratos-api.md), [marketplace público](docs/05-funcionalidades/marketplace-publico.md) e [Design System](docs/04-interface/design-system.md).

## Git

O bootstrap cria um commit local em `main`. A publicação é manual e exige revisar o destino remoto antes de executar `git push`; nenhum push é realizado automaticamente.
