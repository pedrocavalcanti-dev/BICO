# Segurança

Controles existentes: segredos fora do Git; settings separados; produção sem DEBUG e com variáveis obrigatórias; cookies seguros em produção; proteção CSRF e clickjacking do Django; hosts/origens explícitos; permissões DRF autenticadas por padrão; hashing de senha Django; admin de auditoria somente leitura. MySQL usa credenciais de ambiente, conexão `utf8mb4` e um engine único explícito; produção deve usar conta de aplicação com privilégio mínimo, sem root.

Ainda não existem login público, limitação de tentativas, MFA, RBAC operacional ou monitoramento de incidentes. Os 10 testes automatizados da fundação foram executados localmente; eles não substituem testes dos fluxos de autenticação, ainda não implementados. Não declarar segurança absoluta. Revise o check de deploy antes de publicar e atualize este documento quando controles forem implementados.


## Autenticação Alpha 0.3.0

A Web usa sessões nativas Django, rotação da sessão no login, cookies `HttpOnly`/`SameSite=Lax`, cookies `Secure` em produção e CSRF em mutações. Logout só aceita POST. `next` é validado pelo host/protocolo permitidos. Cadastro, recuperação e edição usam formulários allowlist; e-mail é único e o usuário da API deriva sempre da sessão.

Tentativas são limitadas no MySQL compartilhado por IP e identidade, com chaves HMAC e janela temporal. Limites: 12 tentativas de login em 15 minutos; 5 de cadastro e 5 de recuperação por hora. Buckets não guardam IP/e-mail em claro e podem ser limpos com `manage.py cleanup_auth_throttle`; agendar a execução diária. O limite é da aplicação, mas não substitui controles de borda contra tráfego distribuído volumoso.

Auditoria registra os tipos de eventos sem credenciais, token, IP ou conteúdo pessoal. Recuperação usa tokens e formulários nativos Django e resposta neutra. Desenvolvimento grava e-mails no diretório local ignorado pelo Git; produção requer SMTP. Confirmação de e-mail, MFA e autenticação mobile ainda não estão implementadas. Consulte também `docs/05-funcionalidades/contas.md`.
