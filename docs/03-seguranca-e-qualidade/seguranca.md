# Segurança

Controles existentes: segredos fora do Git; settings separados; produção sem DEBUG e com variáveis obrigatórias; cookies seguros em produção; proteção CSRF e clickjacking do Django; hosts/origens explícitos; permissões DRF autenticadas por padrão; hashing de senha Django; admin de auditoria somente leitura. MySQL usa credenciais de ambiente, conexão `utf8mb4` e um engine único explícito; produção deve usar conta de aplicação com privilégio mínimo, sem root.

Ainda não existem login público, limitação de tentativas, MFA, RBAC operacional ou monitoramento de incidentes. Os 10 testes automatizados da fundação foram executados localmente; eles não substituem testes dos fluxos de autenticação, ainda não implementados. Não declarar segurança absoluta. Revise o check de deploy antes de publicar e atualize este documento quando controles forem implementados.
