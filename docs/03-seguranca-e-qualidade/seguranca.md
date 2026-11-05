# Segurança

Controles existentes: segredos fora do Git; settings separados; produção sem DEBUG e com variáveis obrigatórias; cookies seguros em produção; proteção CSRF e clickjacking do Django; hosts/origens explícitos; permissões DRF autenticadas por padrão; hashing de senha Django; admin de auditoria somente leitura. MySQL usa credenciais de ambiente, conexão `utf8mb4` e um engine único explícito; produção deve usar conta de aplicação com privilégio mínimo, sem root.

Na Alpha 0.3.0, cadastro, login e sessão Web usam os mecanismos nativos do Django. Logout é POST com CSRF, `next` é validado, formulários e serializer limitam os campos editáveis e a API deriva o usuário de `request.user`. Recuperação de senha usa token temporário Django e resposta neutra. Tentativas de login, cadastro e recuperação usam buckets HMAC persistidos no MySQL. A auditoria não guarda senha, token, IP ou payload pessoal.

Validação em 2026-11-05: `manage.py check`, `makemigrations --check --dry-run`, Ruff nos módulos alterados e 20 testes focados passaram. A suíte completa encontrou 40 testes, mas o runner não conseguiu criar `test_bico` por falta de privilégio MySQL (erro 1044); portanto, os fluxos que dependem da criação do banco de teste ainda não foram validados integralmente. Não declarar segurança absoluta. Revise o check de deploy antes de publicar.


## Autenticação Alpha 0.3.0

A Web usa sessões nativas Django, rotação da sessão no login, cookies `HttpOnly`/`SameSite=Lax`, cookies `Secure` em produção e CSRF em mutações. Logout só aceita POST. `next` é validado pelo host/protocolo permitidos. Cadastro, recuperação e edição usam formulários allowlist; e-mail é único e o usuário da API deriva sempre da sessão.

Tentativas são limitadas no MySQL compartilhado por IP e identidade, com chaves HMAC e janela temporal. Limites: 12 tentativas de login em 15 minutos; 5 de cadastro e 5 de recuperação por hora. Buckets não guardam IP/e-mail em claro e podem ser limpos com `manage.py cleanup_auth_throttle`; agendar a execução diária. O limite é da aplicação, mas não substitui controles de borda contra tráfego distribuído volumoso.

Auditoria registra os tipos de eventos sem credenciais, token, IP ou conteúdo pessoal. Recuperação usa tokens e formulários nativos Django e resposta neutra. Desenvolvimento grava e-mails no diretório local ignorado pelo Git; produção requer SMTP. Confirmação de e-mail, MFA e autenticação mobile ainda não estão implementadas. Consulte também `docs/05-funcionalidades/contas.md`.
