# Segurança

Controles existentes: segredos fora do Git; settings separados; produção sem DEBUG e com variáveis obrigatórias; cookies seguros em produção; proteção CSRF e clickjacking do Django; hosts/origens explícitos; permissões DRF autenticadas por padrão; hashing de senha Django; admin de auditoria somente leitura.

Ainda não existem login público, limitação de tentativas, MFA, RBAC operacional, monitoramento de incidentes ou testes automatizados executados nesta máquina. Não declarar segurança absoluta. Revise o check de deploy antes de publicar e atualize este documento quando controles forem implementados.
