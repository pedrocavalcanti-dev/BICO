# Tarefa atual

## Alpha 0.1.1 — MySQL e base visual

- [x] Inspecionar instruções, estado do Git, settings, dependências e documentação afetada.
- [x] Confirmar serviço MySQL80 ativo, versão 8.0.46 e porta 3306 acessível.
- [x] Configurar backend MySQL com variáveis `DB_*`, opções de conexão por sessão e produção fail-closed.
- [x] Instalar `mysqlclient` e remover dependência PostgreSQL do ambiente Python.
- [x] Inspecionar e integrar as logos fornecidas; preservar favicon e reservar pasta de banners.
- [x] Preparar CSS tokens/base/componentes/site e documentação do design system.
- [x] Atualizar README, arquitetura, segurança, escopo, roadmap, ADRs, release e backlog.
- [x] Verificar banco `Bico`, schema, charset/collation, engine, SQL mode, isolamento, tabelas e grants.
- [x] Confirmar schema inicialmente vazio e aplicar migrations existentes, sem criar ou apagar o banco.
- [x] Executar checks, 10 testes sem banco temporário, smoke transacional revertido, HTTP local e coleta estática dry-run.
- [x] Revisar diff e criar commit local Alpha 0.1.1.

O check de produção aponta somente HSTS desligado, mantido até domínio/TLS/proxy serem definidos. Produção deve usar credenciais MySQL próprias de privilégio mínimo.
