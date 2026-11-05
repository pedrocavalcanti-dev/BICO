# Contas de cliente — Alpha 0.3.0

## Identidade e cadastro

Existe uma única conta por pessoa. O cadastro em `/cadastrar/` recebe nome, e-mail e senha; o e-mail é normalizado e único. O Django valida a senha e grava somente o hash pelo hasher configurado. Não são solicitados CPF, endereço ou dados de prestador.

Após o cadastro, a conta recebe uma sessão Web e o cliente pode usar a área privada imediatamente. A confirmação de e-mail ainda não está implementada; a interface não marca o endereço como verificado. A ativação como prestador permanece fora desta versão.

## Login e sessão

- `/entrar/` usa autenticação de sessão nativa do Django. O parâmetro `next` só é aceito quando o destino é do mesmo host e protocolo permitido.
- “Manter conectado” define uma sessão persistente de 30 dias; sem essa opção, a sessão termina ao fechar o navegador. A idade padrão é de 14 dias para sessões sem prazo explícito.
- `/sair/` aceita somente POST com CSRF e invalida a sessão.
- Login inválido apresenta mensagem genérica. O Django renova a chave da sessão durante o login.
- Cookies de sessão são `HttpOnly` e `SameSite=Lax`; em produção, sessão e CSRF exigem `Secure`.

## Recuperação e alteração de senha

`/recuperar-senha/` responde de forma neutra, sem informar se o e-mail existe. Os links usam os tokens temporários e assinados do Django. Em desenvolvimento, mensagens são gravadas em `bico_django/.local-emails/`; isso não representa entrega externa. Produção exige SMTP configurado. `/minha-conta/alterar-senha/` exige a senha atual. Tokens e senhas não são escritos na auditoria.

## Área do cliente

- `/minha-conta/` mostra o nome, e-mail, data de cadastro e estado de confirmação (indisponível nesta versão), sem estatísticas inventadas.
- `/minha-conta/editar/` permite alterar apenas o nome. E-mail, UUID, flags administrativas, grupos e permissões não são editáveis por esse formulário.
- Conversas e notificações têm destinos privados com estados vazios informativos; a funcionalidade completa não está implementada.
- O menu de conta compartilhado apresenta a sessão atual, conta, ações ainda futuras e saída por POST.

## Limitação de tentativas e auditoria

O limite usa buckets atômicos no MySQL compartilhado, com chaves HMAC e sem persistir IP/e-mail em claro: login até 12 por IP e identidade em 15 minutos; cadastro e recuperação até 5 por IP e identidade por hora. A resposta de bloqueio inclui `Retry-After`. O comando `python manage.py cleanup_auth_throttle` remove buckets antigos; agende-o periodicamente (por exemplo, diariamente) na operação.

O app `audit` registra sucesso/negação de login, cadastro, logout, pedido/conclusão de redefinição, mudança de senha e atualização de perfil. Metadados guardam apenas o canal; não incluem credenciais, token, IP ou payload de perfil.

## Pendências explícitas

Confirmação de e-mail, MFA, autenticação social, aprovação/modo Prestador, chat, favoritos, notificações reais e contratações permanecem planejados. Cadastro e login de API para mobile também não estão expostos nesta etapa.
