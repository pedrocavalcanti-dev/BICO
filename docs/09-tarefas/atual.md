# Tarefa atual — Alpha 0.3.1: Marketplace Experience Update

- [x] Inspecionar instruções, documentação, Git, modelos de catálogo, seletores, páginas públicas, API, seed e design system.
- [x] Criar `feature/bico-alpha-0.3.1-experience` a partir da branch Alpha 0.3.0, preservando a Home Alpha 0.2.0.
- [x] Limitar as categorias do cabeçalho a sete destaques ativos, com destino para todas as categorias e overflow contido em telas estreitas.
- [x] Refinar detalhes públicos de anúncio e perfil sem inventar avaliações, distância, disponibilidade, verificação ou transações.
- [x] Criar galeria de imagens de anúncio, migration não destrutiva, inline de administração e contrato REST de leitura.
- [x] Melhorar seed idempotente com imagens WebP locais por especialidade e registros claramente demonstrativos.
- [x] Manter solicitações e chat como ações explicativas, protegidas por login, sem criar registros ou simular envio.
- [x] Exibir marca Google como opção desabilitada “Em breve”; nenhum login social foi apresentado como integrado.
- [x] Atualizar documentação de estado, roadmap, banco, API, segurança, navegação, marketplace público, ADR e release.
- [x] Validar `manage.py check`, `makemigrations --check --dry-run`, 22 testes focados de `apps.core.tests`, Ruff nos arquivos Python alterados e `git diff --check`.
- [x] Registrar que a varredura Ruff mais ampla permanece com 29 apontamentos preexistentes em `apps/accounts/admin.py` e migrations iniciais, fora dos arquivos desta entrega.
- [x] Confirmar migration `catalog.0003_servicelistingimage` aplicada no banco local e executar `seed_bico_demo` duas vezes sem duplicação.
- [x] Confirmar respostas HTTP 200 em Home, páginas públicas, endpoints públicos e ativos locais por meio do cliente Django e servidor local.
- [ ] Suíte Django completa encontrou 45 testes, mas ficou bloqueada antes da execução: MySQL retorna erro 1044 ao criar `test_bico` com a conta `bico_app`. Não rodar testes no schema principal nem ampliar privilégio global da conta da aplicação.
- [ ] Revisão visual da Alpha 0.3.1 em 360, 390, 768, 1024 e 1440 px; tentativas com Edge não produziram screenshots nesta sessão.
- [x] Criar o commit `c116678 feat: refine BICO marketplace experience` e publicar `feature/bico-alpha-0.3.1-experience` em `origin`, sem force push.
- [ ] Integrar à `main` somente após a suíte completa passar e a revisão visual final.

Dependência: esta branch deriva de `feature/bico-alpha-0.3.0-auth` no commit `0be5a3e`, que preserva os commits de autenticação e a Home Alpha 0.2.0 (`3702e69`). Pendências de produto permanecem: chat, contratação, avaliações reais, favoritos persistentes, notificações, modo Prestador, confirmação de e-mail, login social e pagamentos. Não usar push forçado nem integrar a `main` enquanto a suíte completa estiver bloqueada.
