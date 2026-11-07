# Segurança

## Refinamento do onboarding — Alpha 0.4.1

A nova interface mantém sessão/CSRF, autorização por proprietário, limites de upload, pré-validação e storage documental privado cifrado da Alpha 0.4.0. Páginas de edição e acompanhamento recebem `never_cache`/`no-store`. Prévia local usa URL temporária em memória; o código não persiste dados em localStorage nem envia documentos a terceiros. O salvamento automático usa os endpoints autenticados existentes e o envio final mantém revisão humana pendente. A consulta ViaCEP recebe somente CEP, sem cookies/referrer da BICO (ADR-011). Produção continua com onboarding/upload desabilitados.

Controles existentes: segredos fora do Git; settings separados; produção sem DEBUG e com variáveis obrigatórias; cookies seguros em produção; proteção CSRF e clickjacking do Django; hosts/origens explícitos; permissões DRF autenticadas por padrão; hashing de senha Django; admin de auditoria somente leitura. MySQL usa credenciais de ambiente, conexão `utf8mb4` e um engine único explícito; produção deve usar conta de aplicação com privilégio mínimo, sem root.

Na Alpha 0.3.0, cadastro, login e sessão Web usam os mecanismos nativos do Django. Logout é POST com CSRF, `next` é validado, formulários e serializer limitam os campos editáveis e a API deriva o usuário de `request.user`. Recuperação de senha usa token temporário Django e resposta neutra. Tentativas de login, cadastro e recuperação usam buckets HMAC persistidos no MySQL. A auditoria não guarda senha, token, IP ou payload pessoal.

Na Alpha 0.3.1, detalhe de anúncio e perfil consultam os seletores públicos existentes: somente anúncios publicados de prestadores aprovados e categorias ativas, e somente perfis aprovados. A galeria expõe apenas imagem e texto alternativo; campos privados do usuário e estados de moderação seguem fora dos serializers. Uploads continuam sujeitos ao validador de extensão e tamanho existente. O seed só preenche imagens ausentes e registros demonstrativos; as imagens de exemplo não são prova de serviço, identidade, aprovação, avaliação ou vínculo comercial.

O botão Google do login é desabilitado e explicitamente futuro; não envia credenciais nem realiza OAuth.

Validação em 2026-11-05: `manage.py check`, `makemigrations --check --dry-run`, Ruff nos módulos alterados e 20 testes focados passaram. A suíte completa encontrou 40 testes, mas o runner não conseguiu criar `test_bico` por falta de privilégio MySQL (erro 1044); portanto, os fluxos que dependem da criação do banco de teste ainda não foram validados integralmente. Não declarar segurança absoluta. Revise o check de deploy antes de publicar.


## Autenticação Alpha 0.3.0

A Web usa sessões nativas Django, rotação da sessão no login, cookies `HttpOnly`/`SameSite=Lax`, cookies `Secure` em produção e CSRF em mutações. Logout só aceita POST. `next` é validado pelo host/protocolo permitidos. Cadastro, recuperação e edição usam formulários allowlist; e-mail é único e o usuário da API deriva sempre da sessão.

Tentativas são limitadas no MySQL compartilhado por IP e identidade, com chaves HMAC e janela temporal. Limites: 12 tentativas de login em 15 minutos; 5 de cadastro e 5 de recuperação por hora. Buckets não guardam IP/e-mail em claro e podem ser limpos com `manage.py cleanup_auth_throttle`; agendar a execução diária. O limite é da aplicação, mas não substitui controles de borda contra tráfego distribuído volumoso.

Auditoria registra os tipos de eventos sem credenciais, token, IP ou conteúdo pessoal. Recuperação usa tokens e formulários nativos Django e resposta neutra. Desenvolvimento grava e-mails no diretório local ignorado pelo Git; produção requer SMTP. Confirmação de e-mail, MFA e autenticação mobile ainda não estão implementadas. Consulte também `docs/05-funcionalidades/contas.md`.

## Documentos do onboarding — Alpha 0.4.0

Uploads de identidade ficam fora de `static/` e de qualquer URL pública. O backend valida os bytes por Pillow, não confia no nome ou Content-Type, aceita JPEG/PNG/WebP, limita 8 MB/25 MP e dimensões, faz verificações heurísticas básicas de brilho/detalhe/desfoque e reprocessa a imagem para remover EXIF. Isso não verifica identidade, autenticidade, CPF, malware ou conteúdo textual.

Os bytes são cifrados com Fernet antes de gravar em storage privado. Desenvolvimento deriva chave local do `DJANGO_SECRET_KEY` e deve usar somente dados sintéticos. Produção requer chaves externas em `BICO_PROVIDER_DOCUMENT_ENCRYPTION_KEYS`, porém o onboarding e uploads são forçados desabilitados. Não abrir coleta real sem revisão jurídica, finalidade/base legal, aviso, retenção/descarte, processo de revisão com acesso restrito, proteção do MySQL e backups e operação/rotação de chaves. O storage de arquivos tem cifragem autenticada; campos privados no banco e backups dependem de controles de infraestrutura ainda não aprovados.

A view de prévia exige login e busca documento apenas pela solicitação relacionada a `request.user`; responde com `private, no-store`, `nosniff` e CSP restritiva. Serializers públicos e autenticados do onboarding não incluem referência ou URL dos arquivos; o serializer de solicitação devolve somente os dados do próprio usuário. Upload e envio usam throttle compartilhado no MySQL (chaves HMAC, dez uploads e cinco envios por usuário/IP por hora). Auditoria registra upload/submissão sem nome, conteúdo, CPF ou payload pessoal.

Quatro testes focados cobrem validação e persistência, mas a execução integrada ficou bloqueada antes de iniciar testes pela falta de privilégio MySQL para criar `test_bico` (1044). Não foram usados SQLite nem o banco principal como substitutos. Veja [onboarding do prestador](../05-funcionalidades/prestadores.md) e [ADR-010](../07-decisoes/ADR-010-documentos-privados-do-prestador.md).
