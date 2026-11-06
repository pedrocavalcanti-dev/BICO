# Tarefa atual — Alpha 0.4.0: onboarding do prestador

- [x] Inspecionar o estado Git e a implementação existente de conta, catálogo, prestadores, API, segurança e design system; partir da branch publicada Alpha 0.3.2.
- [x] Criar `feature/bico-alpha-0.4.0-provider-onboarding`, preservando histórico e migrations existentes.
- [x] Implementar onboarding de cinco etapas com rascunho persistente, identificação PF/PJ, dados profissionais, categorias ativas, modalidades e localização privada.
- [x] Implementar etapa documental com uploads separados de frente/verso RG/CIN/CNH, validação real JPEG/PNG/WebP, limites de tamanho/resolução, pré-validação de imagem, prévia e substituição.
- [x] Armazenar imagens cifradas fora de `static/`, sem URL pública, e restringir prévia ao proprietário autenticado.
- [x] Submeter apenas com dois arquivos válidos; manter `PENDING_REVIEW`/`NOT_REVIEWED` e impedir alteração de campos internos de decisão pela Web/API.
- [x] Adicionar rate limiting MySQL para uploads/envios e auditoria mínima sem dados documentais.
- [x] Integrar entrada na Home e Minha Conta e adicionar endpoints autenticados para progresso, upload e envio.
- [x] Manter onboarding e coleta desabilitados em production settings até aprovação jurídica e revisão de segurança.
- [x] Atualizar README, estado atual, roadmap, banco, segurança, privacidade, funcionalidade de prestadores, API, changelog, índice, ADR e esta tarefa.
- [x] Aplicar a migration não destrutiva `providers.0002_providerapplication_providerdocument_and_more` no MySQL local autorizado.
- [x] Executar `manage.py check`, `makemigrations --check --dry-run`, Ruff nos módulos alterados e `git diff --check`.
- [x] Fazer smoke checks sem banco de testes: JPEG/PNG/WebP, arquivo corrompido, storage cifrado sem URL pública, templates e normalização CPF/CNPJ.
- [ ] Executar os quatro testes de integração focados. O runner parou antes de iniciar por erro MySQL 1044 ao criar `test_bico`; provisionar privilégios limitados ao banco de teste antes de tentar novamente.
- [ ] Fazer revisão visual mobile/desktop do onboarding.
- [x] Revisar diff/segredos, confirmar arquivos locais ignorados e validar `git diff --cached --check`.
- [x] Criar o commit `8fbec3e` e publicar a branch no `origin` sem force push.

Pendências antes de integrar à `main`: executar os quatro testes focados em banco MySQL isolado e revisar visualmente o fluxo em mobile/desktop. Pendências antes de coleta em produção: aprovação jurídica, finalidade e base legal, retenção/descarte, revisão de proteção do MySQL e backups, rotação/recuperação de chaves e operação de revisão.

Implementação publicada em `origin/feature/bico-alpha-0.4.0-provider-onboarding`, commit `8fbec3e`. A `main` não foi alterada porque os testes focados não puderam iniciar.
