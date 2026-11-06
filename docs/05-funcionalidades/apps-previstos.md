# Apps e domínios

| Domínio | Responsabilidade | Estado |
|---|---|---|
| `core` | Home, banners, páginas informativas e conteúdo público | Home e banners implementados; health está em `api.v1` |
| `accounts` | Identidade, autenticação e perfil pessoal | Cadastro, sessão, recuperação de senha e perfil de cliente implementados; confirmação de e-mail e recursos profissionais futuros |
| `audit` | Eventos administrativos/de segurança | Modelo inicial e admin somente leitura |
| `providers` | Perfil público e estado de aprovação de profissionais/empresas | Leitura pública e administração implementadas; ativação/cadastro profissional pendente |
| `catalog` | Categorias e anúncios de serviços | Descoberta, busca, galeria e administração implementadas; publicação por prestadores pendente |
| `service_requests` | Solicitação e transições de contratação | Planejado |
| `messaging` | Conversas, participantes e mensagens | Planejado |
| `reviews` | Avaliações vinculadas a serviço concluído | Planejado |
| `geo` | Região, coordenadas aproximadas e distância | Planejado; endereço preciso protegido |
| `notifications` | Avisos e preferências | Planejado |
| `support`, `moderation` | Atendimento, denúncias e decisões | Planejado |
| `backoffice` | Interface interna BICO Gestão | Planejado |

Criar um app somente quando uma etapa funcional precisar dele; não gerar diretórios vazios como substituto de implementação.
