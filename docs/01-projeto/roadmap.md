# Roadmap

| Versão | Objetivo | Estado |
|---|---|---|
| 0.1.0 | Fundação Django, usuário UUID, API base e documentação | Concluída |
| 0.1.1 | MySQL local/principal, branding e design system inicial | Concluída |
| 0.2.0 | Home do marketplace, catálogo público, perfis, busca, APIs de leitura e seed demonstrativo | Implementada; commit `3702e69`, ancestral da Alpha 0.3.0 |
| 0.3.0 | Cadastro/login, recuperação de senha e área do cliente | Implementada na branch de desenvolvimento; suíte completa bloqueada por privilégio MySQL |
| 0.3.1 | Refinar navegação, imagens, galeria de anúncios, perfil público, contratos API e login Google futuro | Branch `feature/bico-alpha-0.3.1-experience` publicada; validações focadas concluídas; suíte MySQL completa e revisão visual pendentes |
| 0.3.2 | Enriquecer imagens demonstrativas, completar galerias, corrigir associações e refinar anúncio/perfil | Publicada em `origin/feature/bico-alpha-0.3.2-visual-assets`, commit `e857cbb`; 36 capas únicas, 28 testes focados e revisão visual mobile/desktop passaram; suíte completa pendente de privilégio MySQL |
| 0.4.0 | Onboarding de prestador PF/PJ, modalidades, revisão documental e refinamento visual responsivo | Publicada em `origin/feature/bico-alpha-0.4.0-provider-onboarding` (implementação `8fbec3e`); checks de código concluídos, migration aplicada no MySQL local e smoke/revisão responsiva focados; suíte isolada bloqueada pelo privilégio para criar `test_bico`; não integrada à `main` |
| 0.4.1 | Área do Prestador: dashboard, gestão do perfil/atendimento/portfólio e consulta de anúncios | Publicada em `origin/feature/bico-alpha-0.4.1-provider-dashboard`, commit `331ae2b`; 8 testes focados bloqueados por privilégio MySQL para `test_bico`; sem integração à `main` |
| 0.4.2 | Criação, edição, revisão e gerenciamento de anúncios pelo prestador aprovado | Planejada; sem CRUD parcial nesta versão |
| A definir | BICO Gestão: análise humana de onboarding, correções e histórico de decisões | Planejada; depende de revisão jurídica e operacional dos documentos |
| 0.5.0 | Solicitações de serviço e estados de atendimento | Planejada |
| 0.6.0 | Chat e sistema de avaliações e reputação vinculado a serviços concluídos | Planejada |
| 0.7.0 | BICO Agora: descoberta geográfica com Mapbox, sujeita a decisão de precisão, consentimento e privacidade | Planejada |
| 0.8.0 | Moderação automatizada de anúncios, com revisão humana e mecanismos de contestação | Planejada |
| 0.9.0 | PWA, estabilização e preparação técnica da Beta Web | Planejada |

## Metas de calendário

- **Novembro/2026:** desenvolvimento do Modo Prestador, começando pelo onboarding Alpha 0.4.0 e seguindo para a Área do Prestador.
- **Dezembro/2026:** meta de concluir a Beta Web Django, condicionada à conclusão dos fluxos prioritários e das validações necessárias.
- **Janeiro/2027:** iniciar o desenvolvimento dos aplicativos Flutter para Android e iOS, consumindo os contratos da API estabilizados na Web.

Pagamentos e comércio de produtos permanecem fora do escopo atual. BICO Agora com Mapbox depende de decisão sobre precisão, consentimento, dados e privacidade antes de ativar localização geográfica.

O upload de documentos de identidade não pode ser aberto a usuários de produção até aprovação jurídica e conclusão das decisões sobre base/finalidade, retenção/exclusão, proteção do banco e backups, gestão/rotação de chaves e tratamento operacional seguro. A implementação atual mantém o onboarding e o upload desativados nas configurações de produção.
