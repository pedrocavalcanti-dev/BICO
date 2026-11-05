# Arquitetura da API

Prefixo estável: `/api/v1/`. Views REST pertencem a `api/v1/`; cada domínio futuro deve ter serializers, permissões e validação apropriados. DRF exige usuário autenticado por padrão; endpoints explicitamente públicos declaram `AllowAny`.

A autenticação web poderá usar sessão e CSRF. O transporte móvel será decidido antes do Alpha mobile, sem acesso direto do aplicativo ao banco. IDs e propriedade de recursos sempre são validados no servidor.

DRF `AutoSchema` está configurado. Um endpoint OpenAPI navegável e os contratos de domínio serão adicionados quando houver endpoints reais; não publicar rotas fictícias.
