# Padrão de respostas API

Sucesso retorna JSON com campos em `snake_case`. O health check retorna apenas estado de liveness. Erros de validação e autenticação devem seguir status HTTP apropriado e não incluir traceback, tokens, segredos ou dados internos.

Formato comum de erro, paginação e envelope de domínio ainda não foi definido porque só existem dois endpoints simples. Definir e versionar o contrato antes de introduzir recursos de marketplace.
