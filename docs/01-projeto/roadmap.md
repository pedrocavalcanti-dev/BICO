# Roadmap

| Versão | Objetivo | Estado |
|---|---|---|
| 0.1.0 | Fundação Django, usuário UUID, API base e documentação | Concluída |
| 0.1.1 | MySQL local/principal, branding e design system inicial | Concluída |
| 0.2.0 | Home do marketplace, catálogo público, perfis, busca, APIs de leitura e seed demonstrativo | Implementada; commit `3702e69`, ancestral da Alpha 0.3.0 |
| 0.3.0 | Cadastro/login, recuperação de senha e área do cliente | Implementada na branch de desenvolvimento; suíte completa bloqueada por privilégio MySQL |
| 0.3.1 | Refinar navegação, imagens, galeria de anúncios, perfil público, contratos API e login Google futuro | Branch `feature/bico-alpha-0.3.1-experience` publicada; validações focadas concluídas; suíte MySQL completa e revisão visual pendentes |
| 0.3.2 | Enriquecer imagens demonstrativas, completar galerias, corrigir associações e refinar anúncio/perfil | Publicada em `origin/feature/bico-alpha-0.3.2-visual-assets`, commit `e857cbb`; 36 capas únicas, 28 testes focados e revisão visual mobile/desktop passaram; suíte completa pendente de privilégio MySQL |
| 0.4.0 | Onboarding de prestador, dados PF/PJ, modalidades e revisão documental humana | Implementação e checks de código concluídos; migration aplicada no MySQL local; testes de integração bloqueados por privilégio para criar `test_bico`; não integrada à `main` |
| 0.4.1 | Área do Prestador, gestão de perfil profissional e controles BICO Gestão | Planejada |
| 0.4.2 | Publicação e gestão de anúncios pelo prestador | Planejada |
| 0.5.0 | Solicitações de serviço e estados de atendimento | Planejada |
| 0.6.0 | Chat e avaliações verificáveis vinculadas ao serviço | Planejada |
| 0.7.0 | Busca geográfica com dados e privacidade adequados | Planejada |
| 0.8.0 | PWA, estabilização e preparação de aplicativos | Planejada |

Flutter Android/iOS consumirá contratos da API após os fluxos web estabilizarem. Pagamentos e comércio de produtos permanecem fora do escopo atual. O mapa não será ativado até existir uma decisão sobre fonte de dados, precisão e consentimento.

O upload de documentos de identidade não pode ser aberto a usuários de produção até aprovação jurídica e conclusão das decisões sobre base/finalidade, retenção/exclusão, proteção do banco e backups, gestão/rotação de chaves e tratamento operacional seguro. A implementação atual mantém o onboarding e o upload desativados nas configurações de produção.
