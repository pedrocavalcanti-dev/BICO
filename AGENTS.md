# Instruções para agentes

## Contexto

BICO é um marketplace bilateral de serviços, iniciado em Campinas-SP. Uma conta pode atuar como cliente e também habilitar um perfil profissional. O Alpha não inclui produtos, pagamentos, chat real ou aplicativos Flutter.

## Antes de alterar

1. Leia `docs/indice.md`, `docs/01-projeto/estado-atual.md` e os documentos do domínio afetado.
2. Inspecione o código e o Git antes de editar. Faça mudanças incrementais e limitadas à tarefa.
3. Use inglês em código, nomes técnicos, apps, campos e endpoints; português brasileiro na interface e documentação.

## Estrutura

- Django e API: `bico_django/`.
- Apps Django: `bico_django/apps/`.
- Rotas versionadas: `bico_django/api/v1/`.
- Templates e arquivos estáticos: `bico_django/templates/` e `bico_django/static/`.
- Mobile futuro: `mobile/` (não criar um app Flutter sem solicitação).
- Documentação: `docs/`.
- Configuração de deploy ainda não escolhida; não introduzir serviços externos por conveniência.

Nunca coloque `manage.py`, `config`, `apps`, `templates` ou `static` diretamente na raiz do monorepo.

## Convenções e banco

- Django segue convenções oficiais; nomes de módulos e classes em inglês.
- O usuário customizado é `accounts.User`; não altere `AUTH_USER_MODEL` depois da primeira migração publicada.
- PostgreSQL é o banco local e principal. Não use SQLite como fallback nem faça operações destrutivas no banco.
- Toda mudança de modelo requer migration versionada e revisão da documentação do banco.
- UUID é usado em entidades públicas quando apropriado; datas devem ser timezone-aware.
- Não criar apps vazios, endpoints simulados ou funcionalidades descritas como implementadas antes de existirem.

## Segurança

- Segredos vêm do ambiente/`.env` local e nunca entram no Git, logs, respostas ou documentação.
- Configuração de produção deve falhar sem secret, banco, hosts e origens confiáveis válidos; nunca habilitar `DEBUG` em produção.
- DRF exige autenticação por padrão; rotas públicas devem declarar explicitamente a permissão pública.
- Validar autorização e propriedade de recursos no backend. Nunca confiar em permissões vindas do navegador.
- Minimizar dados pessoais. Não exigir CPF nem expor endereço residencial preciso.
- Não registrar senhas, tokens, conteúdo de mensagens ou payloads pessoais indiscriminadamente.
- Não alegar verificação, pagamento, criptografia ponta a ponta ou controles ainda não implementados.

## Desenvolvimento e validação

- Ambiente principal: Windows/PowerShell; Python 3.12+.
- Instale dependências com `python -m pip install -r requirements.txt` dentro de `.venv`.
- Execute checks, migrations e testes focados apropriados à alteração. Não declare sucesso de banco sem PostgreSQL conectado.
- Verifique alterações no `git diff`, `.gitignore` e ausência de segredos antes do commit.
- Não sobrescreva histórico, não use `push --force` e não publique sem autorização explícita.

## Documentação e entrega

- Atualize `estado-atual.md`, `docs/09-tarefas/atual.md` e documentos afetados quando a implementação mudar.
- Registre decisões arquiteturais duradouras em ADRs numerados.
- Na entrega, informe implementação, comandos e resultados reais, limitações do ambiente e próxima etapa. Diferencie claramente feito, planejado e pendente.
