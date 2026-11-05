# Ambientes e deploy

## Local

`.env` na raiz, ignorado pelo Git. `manage.py` seleciona `config.settings.development`; DEBUG e hosts podem ser configurados por ambiente. O banco continua PostgreSQL.

## Produção

Use `DJANGO_SETTINGS_MODULE=config.settings.production`. O processo falha sem secret, credenciais completas do PostgreSQL, hosts específicos e origens CSRF explícitas. `DEBUG=False`, cookies seguros e redirecionamento HTTPS são aplicados. HSTS começa desligado e só deve ser habilitado após confirmar domínio, TLS e comportamento do proxy.

Hospedagem, servidor WSGI/ASGI, armazenamento, observabilidade e pipeline ainda não foram escolhidos. Não presumir proxy confiável nem habilitar CORS global.
