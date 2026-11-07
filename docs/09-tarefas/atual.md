# Tarefa atual — Área do Prestador Alpha 0.4.1

- [x] Implementar shell profissional com sidebar recolhível/drawer responsivo, busca funcional nos serviços próprios e retorno ao modo Cliente.
- [x] Exigir perfil realmente aprovado nas views e API; redirecionar anônimo, onboarding em rascunho e solicitação pendente conforme os fluxos existentes; bloquear suspensos/reprovados.
- [x] Dashboard com contagens reais de anúncios, estados vazios de visualizações, atividades auditadas e ações calculadas por dados faltantes; sem gráficos/contadores fictícios.
- [x] Implementar consulta, busca, filtros e paginação de anúncios próprios, sem criar CRUD incompleto.
- [x] Implementar edição allowlist do perfil público (nome, descrição, foto e especialidades), prévia pública/privada, modalidades/região aproximada e configurações.
- [x] Criar portfólio privado com validação/re-encode, limite de 20 imagens, prévia protegida por proprietário, remoção e ordenação.
- [x] Adicionar `GET /api/v1/providers/me/dashboard/` e `GET/PATCH /api/v1/providers/me/profile/` com autenticação, autorização e campos restritos.
- [x] Criar migration não destrutiva `providers.0003_providerportfolioimage` e aplicá-la no MySQL local; `showmigrations` confirma 0001–0003 aplicadas.
- [ ] Suíte focada `apps.providers.test_dashboard`: localizada com 8 testes, mas não iniciou porque a conta MySQL não tem permissão para criar `test_bico` (1044). Nenhum teste foi executado no schema principal; repetir ao provisionar privilégio restrito para o banco isolado.
- [ ] Revisão visual manual em navegador desktop/mobile ainda pendente.
- [x] Validar e revisar diff/ignorados; `.env`, uploads privados, mídia local, logs e artefatos estão fora do Git.
- [x] Criar e publicar o commit `331ae2b` na branch `feature/bico-alpha-0.4.1-provider-dashboard`.
- [ ] Revisão visual manual em navegador desktop/mobile ainda pendente; nenhuma integração à `main` foi feita.

Próxima versão: **Alpha 0.4.2 — criação e gerenciamento completo de anúncios**. BICO Gestão, pedidos, chat, notificações, avaliações e financeiro não fazem parte desta entrega.

## Histórico concluído — correções finais do onboarding Alpha 0.4.0

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
