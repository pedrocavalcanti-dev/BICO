# Apps e domínios

| Domínio | Responsabilidade | Estado |
|---|---|---|
| `core` | Home, conteúdo público e health | Home implementada; health está em `api.v1` |
| `accounts` | Identidade, autenticação e perfil pessoal | Usuário customizado; fluxos ainda pendentes |
| `audit` | Eventos administrativos/de segurança | Modelo inicial e admin somente leitura |
| `providers` | Perfil e disponibilidade profissional | Planejado |
| `catalog` | Categorias e anúncios de serviços | Planejado |
| `service_requests` | Solicitação e transições de contratação | Planejado |
| `messaging` | Conversas, participantes e mensagens | Planejado |
| `reviews` | Avaliações vinculadas a serviço concluído | Planejado |
| `geo` | Região, coordenadas aproximadas e distância | Planejado; endereço preciso protegido |
| `notifications` | Avisos e preferências | Planejado |
| `support`, `moderation` | Atendimento, denúncias e decisões | Planejado |
| `backoffice` | Interface interna BICO Gestão | Planejado |

Criar um app somente quando uma etapa funcional precisar dele; não gerar diretórios vazios como substituto de implementação.
