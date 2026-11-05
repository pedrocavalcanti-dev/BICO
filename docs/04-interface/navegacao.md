# Navegação BICO

Fluxo público: Home → busca/categoria → lista de profissionais/anúncios → perfil ou detalhe. Ações pessoais encaminham o visitante a `/entrar/` com retorno seguro ao caminho solicitado. O cadastro está em `/cadastrar/`.

Com sessão ativa, o header mostra o menu acessível da conta, o acesso a `/minha-conta/` e saída por POST/CSRF. Conversas e notificações encaminham a destinos privados com estado informativo, sem simular recursos completos ou contadores.

Solicitações, chat, favoritos, notificações reais e modo Prestador permanecem futuros. BICO Gestão será uma aplicação interna separada da experiência pública, mas compartilhará backend e identidade central.
