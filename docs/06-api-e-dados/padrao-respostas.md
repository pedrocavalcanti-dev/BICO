# Padrão de respostas API

Sucesso retorna JSON com campos em `snake_case`. O health check retorna apenas estado de liveness. Erros de validação e autenticação devem seguir status HTTP apropriado e não incluir traceback, tokens, segredos ou dados internos.

Rotas paginadas usam o envelope padrão DRF: `count`, `next`, `previous`, `results`. Listagens limitam `page_size` a 48. Erros de parâmetros inválidos usam HTTP 400; recursos não publicáveis ou inexistentes usam 404. A Home retorna arrays limitados por seção sem paginação. Não há envelope próprio adicional nesta versão.
