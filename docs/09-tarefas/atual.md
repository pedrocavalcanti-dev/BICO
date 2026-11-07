# Tarefa atual — correções finais do onboarding Alpha 0.4.0

- [x] Preservar o novo design das cinco etapas e o backend já implementado. O refinamento visual solicitado anteriormente como Alpha 0.4.1 estava sem commit e foi levado à branch de entrega solicitada, sem descartar alterações.
- [x] Corrigir o Enter exclusivamente na busca de especialidades. O envio implícito acionava o primeiro submit do formulário, “Salvar e sair”. Os botões já tinham `type` explícito.
- [x] Preservar Enter na textarea e nos botões Continuar/Salvar e sair, inclusive durante navegação por teclado.
- [x] Atualizar o título para “Tenho uma empresa ou MEI”, mantendo `COMPANY`/CNPJ e somente duas opções.
- [x] Preservar JPG/PNG/WebP para frente/verso de RG/CIN/CNH. Documentar PDF empresarial adicional como futuro, condicionado a processamento seguro, sem habilitar seu envio.
- [x] Revisar a etapa 5: rascunho, imagem salva para análise, envio pendente e substituição necessária são distintos; uma foto tecnicamente legível não é apresentada como documento aprovado. Solicitação enviada permanece `PENDING_REVIEW`/`NOT_REVIEWED`.
- [x] Executar somente `manage.py check` e 16 verificações focadas nesta correção; todos passaram. Teclado conferido em 390/1440 px; formatos reais e rejeição de PDF conferidos no backend; renderização dos estados e manutenção de PF/PJ conferidas. Sem escrita no banco e sem repetir a bateria anterior.
- [x] Revisar diff e arquivos ignorados antes de preparar o commit. `.env`, uploads privados e artefatos não integram a entrega.

Branch de entrega: `feature/bico-alpha-0.4.0-provider-onboarding`, a partir de `e415242`. Commit e publicação na mesma branch foram autorizados; hashes e confirmação remota constam do histórico Git e do relatório de entrega. Sem force push ou integração à `main`.

As validações anteriores do novo design permanecem registradas em `estado-atual.md`: 66 verificações de fluxo MySQL com rollback e 43 de navegador. Os ajustes finais foram verificados separadamente em `artifacts/onboarding-ux/final-fixes-results.json` (arquivo local ignorado pelo Git). A suíte completa em banco isolado `test_bico` continua pendente de privilégios; não foi repetida aqui.

Coleta real em produção continua desabilitada. Área do Prestador, BICO Gestão e publicação de serviços permanecem futuras. Nenhum dashboard foi iniciado.
