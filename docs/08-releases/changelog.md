# Changelog

## Correções finais do onboarding Alpha 0.4.0 — 2026-11-06

- Incorporado o novo design anteriormente validado e ainda não commitado à mesma branch de desenvolvimento da Alpha 0.4.0, preservando seu histórico.
- Enter na busca de especialidades impede apenas o submit implícito desse campo; demais usos de Enter mantidos. Todos os botões do fluxo têm tipo explícito.
- Opção “Tenho uma empresa ou MEI” continua `COMPANY`/CNPJ. JPG/PNG/WebP preservados; PDF empresarial adicional registrado como futuro, sem habilitação.
- Revisão esclarece rascunho, imagem salva para análise e necessidade de envio/substituição, sem indicar aprovação documental. Solicitação enviada permanece pendente de análise humana.
- `manage.py check` e 16 verificações focadas passaram, sem escrita no banco. Sem redesenho adicional, mudança de backend, force push ou merge automático.

## 0.4.1-alpha — Área do Prestador — 2026-11-06

- Criado dashboard autenticado apenas para `ProviderProfile` aprovado, com redirecionamento coerente para login/onboarding/acompanhamento e bloqueio de perfis suspensos ou não aprovados.
- Adicionados dashboard responsivo, navegação recolhível/drawer, busca e listagem de anúncios próprios, edição do perfil público permitido, área aproximada de atendimento, configurações e prévias pública/privada.
- Indicadores contam anúncios reais. Visualizações e gráfico ficam explicitamente indisponíveis; atividades vêm da auditoria; estados vazios não inventam pedidos, faturamento, avaliação ou mensagem.
- Portfólio aceita até 20 imagens, com verificação/re-encode WebP e storage privado cifrado; leitura, exclusão e ordenação exigem sessão, aprovação e propriedade.
- API v1 adiciona dashboard e perfil `me`, restritos a sessão e aprovação, com serializer allowlist e auditoria mínima.
- Migration não destrutiva `providers.0003_providerportfolioimage` adiciona galeria privada.
- `manage.py check`, `makemigrations --check --dry-run`, Ruff check/format e smoke de templates/rotas passaram; migration `0003` aplicada no MySQL local. Oito testes focados não iniciaram por MySQL 1044 ao criar `test_bico`; não houve escrita de testes no banco principal. Inspeção visual em navegador ainda pendente.
- CRUD de anúncios, tracking, BICO Gestão, pedidos, chat, notificações, avaliações e financeiro permanecem futuros.

## Refinamento de UX do onboarding Alpha 0.4.0 — 2026-11-06

- Refatorado o frontend do onboarding em tela dedicada, com trilha lateral, progresso mobile, identidade BICO, SVGs locais, cards compactos e microinterações com movimento reduzido.
- Documentos passaram à identificação, com prévia, substituição, arrastar/soltar e feedback do envio privado. Opcionais recolhidos; especialidades agrupadas com busca/limite; atendimento contextual com CEP ViaCEP, fallback manual e raio visual.
- Salvamento automático de etapas válidas pela API existente, confirmação após resposta do servidor e ação Salvar e sair. Fluxo POST sem JavaScript preservado.
- Revisão e sucesso redesenhados, ciência da análise humana e estimativa variável de até 24h. `PENDING_REVIEW`/`NOT_REVIEWED`, armazenamento cifrado e bloqueio de produção preservados; sem aprovação automática ou perfil público novo.
- Sem mudança de modelos ou migrations. Forms receberam ajustes de labels/validação, categoria principal ativa e cidade/UF únicos no editor. Rotas privadas usam `no-store`.
- Smoke PF/PJ controlado no MySQL com 66 asserções e rollback; renderização em cinco larguras e interações do navegador verificadas. Suíte completa isolada permanece pendente de privilégios de `test_bico` e não foi repetida nesta tarefa visual.
- Refinamento incorporado na branch `feature/bico-alpha-0.4.0-provider-onboarding`, derivada de `e415242`; mantém a versão Alpha 0.4.0 do onboarding.

## 0.4.0-alpha — 2026-11-06

- Implementado onboarding progressivo do prestador em cinco etapas, com persistência de rascunho, PF/PJ, validação de CPF/CNPJ e telefone, categorias do banco, modalidades combináveis e localização privada.
- Etapa 5 recebe duas imagens legíveis de RG/CIN/CNH (frente e verso), reconhece JPEG/PNG/WebP por conteúdo, limita tamanho/resolução e faz pré-validação visual básica. A imagem pode ser substituída antes do envio; não há OCR ou aprovação automática.
- Documentos são reprocessados sem EXIF, cifrados com Fernet em storage sem URL pública e acessíveis pela prévia autenticada do proprietário. Throttle de upload/envio usa contadores HMAC compartilhados no MySQL; auditoria não guarda PII ou arquivos.
- Envio mantém `PENDING_REVIEW`/`NOT_REVIEWED`; a interface informa “Aguardando verificação documental e aprovação”. Estados de decisão e campos de revisão existem apenas para operação interna futura.
- API autenticada para consultar/atualizar etapas, enviar imagens e submeter; integração com Minha Conta e CTA da Home. Produção mantém onboarding e upload desabilitados até revisão jurídica e de segurança.
- Migration não destrutiva `providers.0002_providerapplication_providerdocument_and_more`; arquivos ignorados por Git em `.private-media/`.
- Migration aplicada no MySQL local. `manage.py check`, `makemigrations --check --dry-run`, Ruff nos módulos alterados e `git diff --check` passaram; smoke checks sem banco passaram para formatos, storage cifrado, templates e normalização CPF/CNPJ.
- Quatro testes focados não iniciaram por erro MySQL 1044 na criação de `test_bico`; nenhum teste usou SQLite ou o banco principal.
- Pendentes: validar persistência/autorização com privilégio restrito para banco de teste, revisão visual responsiva, decisão jurídica e controles de retenção, banco/backups e chaves antes de produção.

## 0.3.2-alpha — 2026-11-05

- Adicionados 81 assets WebP gerados localmente para demonstração: 60 fotografias de trabalho, seis imagens avulsas, 12 retratos de profissionais e três logos de empresas fictícias; total de 4.303.738 bytes. Origem e mapa estão em `bico_django/static/marketplace/demo/README.md`.
- Seed demonstrativo passou a completar 36 anúncios publicados com capas e galerias distintas (41 imagens de galeria), cobrir todas as 12 categorias e dar avatar/logo aos 18 perfis demonstrativos. Associações, especialidades e apresentações foram alinhadas; arquivos personalizados e registros reais são preservados.
- Seed reconhece o sufixo aleatório que o armazenamento adiciona aos nomes e continua idempotente sem substituir mídia personalizada.
- Perfil profissional apresenta cards de serviço mais largos, portfólio em grade e profissionais relacionados em cards compactos. Empresas exibem logo próprio sem distorção; a rolagem horizontal da Home fica sem barra visível em desktop.
- O admin exige duas imagens distintas para publicar um anúncio novo ou promover um rascunho. Rascunhos e anúncios anteriormente publicados seguem editáveis. Sem alterações de modelo ou migrations; APIs existentes permanecem compatíveis.
- Validações: `manage.py check`, `makemigrations --check --dry-run`, 28 testes focados (`apps.catalog.tests` e `apps.core.tests`), Ruff nos quatro arquivos Python alterados e inspeção dos 81 WebP passaram. O seed foi repetido no MySQL local sem criar registros.
- Revisão visual em navegador com viewport de 412 px e 1440 px passou para Home, anúncio e perfil, sem largura horizontal excedente. A suíte completa com banco isolado permanece pendente: a conta MySQL atual não pode criar `test_bico` (erro 1044). Não houve teste contra o schema principal nem integração à `main`.
- Implementação publicada em `origin/feature/bico-alpha-0.3.2-visual-assets`, commit `e857cbb`. A `main` não foi alterada enquanto a suíte completa aguarda o privilégio MySQL de teste.

## 0.3.1-alpha — 2026-11-05

- Cabeçalho mostra categorias destacadas gerenciáveis no banco, até sete, e “Todas as categorias”; navegação horizontal fica restrita ao componente em telas estreitas.
- Detalhes públicos de serviço incluem galeria responsiva e acessível, resumo, prestador, localização, preço configurado, descrição, estado vazio de avaliações e serviços relacionados.
- Perfil público inclui especialidades, apresentação, anúncios, portfólio baseado em galeria, estado vazio de avaliações e perfis relacionados por região/categoria; sem distância, nota, verificação ou disponibilidade inventadas.
- `ServiceListingImage` e migration não destrutiva `catalog.0003_servicelistingimage`; API de anúncio expõe galerias e detalhe de prestador inclui anúncios publicados.
- Seed idempotente passou a preencher apenas imagens ausentes em registros demonstrativos; imagens geradas foram otimizadas em WebP e documentadas. Login apresenta Google como opção visual desabilitada, sem OAuth.
- `check`, verificação de migrations, 22 testes focados de `apps.core.tests`, Ruff nos Python alterados e `git diff --check` passaram. A migration consta aplicada no MySQL local e o seed foi executado duas vezes sem duplicação. A suíte completa continua bloqueada pelo erro MySQL 1044 ao criar `test_bico`; há SQL com escopo restrito documentado em `testes-e-qa.md`. Não integrar à `main` até executar todos os testes no banco isolado e concluir revisão visual responsiva.
- Branch publicada: `feature/bico-alpha-0.3.1-experience`, commit `c116678`.

## 0.3.0-alpha — 2026-11-05

- Cadastro de conta única de cliente, login por sessão Django, logout POST/CSRF e área privada para consultar/editar o nome.
- Recuperação e alteração de senha com formulários, validadores e tokens nativos Django; e-mail em arquivo local no desenvolvimento e SMTP obrigatório em produção.
- Throttle persistido no MySQL, auditoria de eventos sem credenciais/PII, API autenticada `GET/PATCH /api/v1/users/me/` e header contextual à sessão.
- Login/cadastro responsivos com identidade BICO e links internos antigos encaminhados às rotas de conta.
- `check`, verificação de migrations, Ruff e 20 testes focados passaram. A suíte completa ainda não inicia por falta de privilégio do usuário MySQL para criar `test_bico` (1044); por isso, a integração à `main` depende dessa validação.
- Confirmação de e-mail, social login, modo Prestador, contratações, chat e notificações reais continuam pendentes.

## 0.2.0-alpha — 2026-11-04

- Home de marketplace dirigida por MySQL, busca e páginas públicas de serviços e prestadores.
- Modelos/admin de banners, categorias, perfis de profissionais/empresas e anúncios de serviços.
- API pública de leitura paginada e serializers de campos públicos.
- Seed demonstrativo seguro para desenvolvimento, sem imagens externas nem avaliações inventadas.
- Fontes locais Inter e Quicksand, CSS responsivo, área geográfica apenas visual e documentação atualizada.
- 21 testes sem banco temporário; migrations aplicadas ao schema MySQL local existente.

## 0.1.1-alpha — 2026-11-04

- Decisão vigente de MySQL, backend Django e driver `mysqlclient`; servidor 8.0.46 validado e migrations aplicadas ao schema vazio `bico`.
- Tokens CSS, estilos base/componentes, integração das logos fornecidas e uso dos favicons existentes.
- Documentação atualizada para registrar a mudança desde PostgreSQL e preparar a futura Home de serviços.

## 0.1.0-alpha — 2026-11-04

- Inicialização do monorepositório Django e documentação arquitetural.
- Usuário customizado UUID/e-mail, apps iniciais, API v1 e Home mínima.
- PostgreSQL foi configurado, mas não estava disponível no ambiente local para migrations aplicadas.
