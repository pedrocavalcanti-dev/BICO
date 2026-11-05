# ADR-006 — MySQL como banco principal

- **Estado:** aceito; substitui ADR-003.
- **Data:** 2026-11-04.

## Contexto

A fundação 0.1.0 configurou PostgreSQL, mas esse servidor não estava disponível no ambiente local. O responsável pelo projeto informou que MySQL já está instalado e que o banco `Bico` foi criado. A decisão é seguir com o banco disponível, preservando models e migrations já existentes.

## Decisão

Usar MySQL 8.0.11 ou superior em desenvolvimento e produção, pelo backend oficial `django.db.backends.mysql` e pelo driver `mysqlclient`. Não manter fallback para PostgreSQL ou SQLite. Usar `utf8mb4`, modo SQL estrito, InnoDB nas novas tabelas e isolamento `READ COMMITTED` por conexão.

As credenciais vêm de variáveis `DB_*` no ambiente ou `.env` local. Produção usa conta de aplicação com privilégio mínimo; nunca root. Não alterar variáveis globais do servidor nem criar, apagar ou recriar o banco sem necessidade.

## Consequências

- A conexão e as permissões precisam ser verificadas antes de aplicar migrations ao banco existente.
- Uma troca futura de banco requer novo ADR e validação das diferenças de collation, índices e constraints.
- A busca geográfica será avaliada com as opções disponíveis para MySQL quando o recurso for especificado.
- `mysqlclient` é uma dependência nativa; usar wheels compatíveis com a versão de Python/plataforma em desenvolvimento.
