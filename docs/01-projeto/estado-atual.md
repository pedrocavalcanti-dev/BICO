# Estado atual

**Versão:** 0.1.1-alpha

**Atualizado:** 2026-11-04

**Ambiente inspecionado:** Windows, PowerShell, Python 3.12.10, Git 2.55.0, MySQL Server 8.0.46

## Implementado nesta etapa

- Backend oficial configurado como MySQL, sem fallback para PostgreSQL/SQLite.
- Driver `mysqlclient==2.3.0` instalado; dependência e pacote psycopg removidos.
- Opções de conexão para utf8mb4, SQL estrito, InnoDB por sessão, isolamento READ COMMITTED e timeout.
- Configuração de produção exige credenciais `DB_*`, host/CSRF explícitos e recusa outro engine.
- Logos oficiais localizadas em `bico_django/static/branding/logos/`; favicon existente preservado e referenciado no template base.
- CSS organizado em tokens, base, componentes e estilos da Home mínima; diretrizes de identidade e Home documentadas.
- ADR-006 registra MySQL como decisão vigente; ADR-003 preservado como histórico substituído.

## Validado

- Serviço `MySQL80` ativo; MySQL Server 8.0.46 em `127.0.0.1:3306`.
- Banco configurado como `Bico`; o nome retornado pelo servidor é `bico`, equivalente no Windows com `lower_case_table_names=1`. Nenhum banco adicional foi criado.
- Schema em `utf8mb4`/`utf8mb4_0900_ai_ci`; default engine InnoDB; conexão em `READ-COMMITTED` com `STRICT_TRANS_TABLES`, `ERROR_FOR_DIVISION_BY_ZERO` e `NO_ENGINE_SUBSTITUTION`.
- Usuário local `bico_app` tem `USAGE` global e `ALL PRIVILEGES` apenas no schema `bico`; não recebeu grants globais. Produção deverá usar credenciais próprias de privilégio mínimo.
- `mysqlclient==2.3.0` importado no Python 3.12 x64; psycopg removido do ambiente e das dependências. `pip check` sem conflitos.
- O schema estava vazio antes das migrations. As 20 migrations esperadas foram aplicadas; todas aparecem aplicadas em `showmigrations`.
- 11 tabelas criadas, todas InnoDB e `utf8mb4_0900_ai_ci`, incluindo `accounts_user`, tabelas de permissões, `audit_auditevent` e `django_migrations`. FKs do usuário e auditoria conferidas.
- Operação transacional de usuário UUID + evento de auditoria/JSON passou e foi revertida; nenhum registro de smoke test permaneceu.
- `manage.py check`, `makemigrations --check --dry-run` e 10 testes passaram. Os testes usam `SimpleTestCase`; não requereram banco temporário nem privilégios globais de CREATE DATABASE.
- HTTP local: Home, API raiz, health, tela de login do admin, CSS, logos e favicon responderam 200; `/admin/` redireciona para login, como esperado sem sessão autenticada.
- `collectstatic --dry-run` identificou os arquivos do projeto e Django/DRF; o diretório `staticfiles` não foi gerado pelo dry-run.
- `check --deploy` apontou apenas HSTS desligado (`security.W004`), que fica pendente até domínio/TLS/proxy serem definidos.
- `.env` está ignorado e fora do Git; variáveis PostgreSQL antigas foram removidas do arquivo local sem exibir credenciais.
- Duas logos oficiais foram encontradas e integradas. Favicon existente foi preservado; pasta de banners reservada, sem arte oficial.

## Pendências

- Revisar a paleta com o arquivo Figma original, que não está no repositório; os tokens atuais seguem as referências visuais anexadas.
- Receber banners oficiais; a pasta está reservada, sem arte inventada.
- Criar superuser interativamente apenas quando o responsável precisar entrar no Django Admin.
- Escolher hosting, proxy, servidor WSGI/ASGI e storage antes do deploy; habilitar HSTS só após domínio/TLS e proxy estarem definidos.

## Próxima etapa

Implementar Alpha 0.2.0: cadastro, login, logout, recuperação de senha e perfil pessoal. A Home BICO 2.0 permanece planejada para depois dos domínios de catálogo/prestadores/anúncios, com dados reais do backend.
