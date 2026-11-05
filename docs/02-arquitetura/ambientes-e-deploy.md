# Ambientes e deploy

## Local

`.env` na raiz, ignorado pelo Git. `manage.py` seleciona `config.settings.development`; DEBUG e hosts podem ser configurados por ambiente. O banco é MySQL; preencha `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` e `DB_PORT` localmente. O engine aceito é `mysql` e não há fallback.

## Produção

Use `DJANGO_SETTINGS_MODULE=config.settings.production`. O processo falha sem secret, credenciais completas do MySQL, hosts específicos e origens CSRF explícitas. `DEBUG=False`, cookies seguros e redirecionamento HTTPS são aplicados. HSTS começa desligado e só deve ser habilitado após confirmar domínio, TLS e comportamento do proxy. Use conta de aplicação com privilégios mínimos, nunca root.

Hospedagem, servidor WSGI/ASGI, armazenamento, observabilidade e pipeline ainda não foram escolhidos. Não presumir proxy confiável nem habilitar CORS global.
