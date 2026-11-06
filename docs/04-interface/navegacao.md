# Navegação BICO

Fluxo público: Home → busca/categoria → lista de profissionais/anúncios → perfil ou detalhe. Ações pessoais encaminham o visitante a `/entrar/` com retorno seguro ao caminho solicitado. O cadastro está em `/cadastrar/`.

Com sessão ativa, o header mostra o menu acessível da conta, o acesso a `/minha-conta/` e saída por POST/CSRF. Conversas e notificações encaminham a destinos privados com estado informativo, sem simular recursos completos ou contadores.

Desde a Alpha 0.3.1, a faixa do cabeçalho apresenta no máximo sete categorias ativas destacadas no banco e o link “Todas as categorias”. A seleção é administrada pelo campo de destaque da categoria; em telas estreitas a rolagem horizontal fica limitada à própria faixa.

O detalhe do anúncio leva à página pública do perfil e oferece ações “Solicitar serviço”/“Conversar com profissional”. Ambas exigem sessão e conduzem a uma explicação de indisponibilidade; não criam solicitações nem enviam mensagens. Perfil e anúncio mostram portfólio/galeria quando há imagens e estados vazios claros para avaliações.

Solicitações, chat, favoritos, notificações reais e modo Prestador permanecem futuros. BICO Gestão será uma aplicação interna separada da experiência pública, mas compartilhará backend e identidade central.
