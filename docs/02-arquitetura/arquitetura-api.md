# Arquitetura da API

Prefixo estável: `/api/v1/`. Views REST pertencem a `api/v1/`; cada domínio futuro deve ter serializers, permissões e validação apropriados. DRF exige usuário autenticado por padrão; endpoints explicitamente públicos declaram `AllowAny`.

A autenticação web poderá usar sessão e CSRF. O transporte móvel será decidido antes do Alpha mobile, sem acesso direto do aplicativo ao banco. IDs e propriedade de recursos sempre são validados no servidor.

DRF `AutoSchema` está configurado. Um endpoint OpenAPI navegável e os contratos de domínio serão adicionados quando houver endpoints reais; não publicar rotas fictícias.

Na Alpha 0.3.1, os serializers públicos de anúncios incluem imagens da galeria. O serializer do detalhe do prestador inclui até 12 anúncios publicados e suas galerias; serializers de listagem/home não fazem essa expansão. Web e API reutilizam os seletores `public_listings()` e `public_providers()`, preservando os filtros de publicação e aprovação.
