# Prestadores — onboarding Alpha 0.4.0 e Área do Prestador Alpha 0.4.1

## Área do Prestador — Alpha 0.4.1

A área profissional utiliza a conta BICO existente e exige sessão autenticada com `ProviderProfile.status=APPROVED`. Visitantes são encaminhados ao login; rascunhos seguem ao onboarding, solicitações pendentes à página de acompanhamento e perfis suspensos/reprovados recebem bloqueio. A aprovação é verificada no backend em cada rota; o modo de interface não concede autorização.

Rotas Web implementadas: `/prestador/painel/`, `/prestador/servicos/`, `/prestador/perfil/`, `/prestador/perfil/previa/`, `/prestador/portfolio/`, `/prestador/atendimento/` e `/prestador/configuracoes/`. O shell compartilhado tem sidebar recolhível no desktop e drawer em telas móveis, busca funcional nos próprios anúncios, alternância ao marketplace e navegação responsiva.

O dashboard calcula anúncios publicados, rascunhos e pausados do perfil autenticado. Visualizações aparecem indisponíveis porque não há coleta de audiência. O gráfico é um estado vazio explicativo; atividades recentes vêm da auditoria real permitida; próximas ações dependem de campos efetivamente ausentes. Não há contadores de pedidos, receita, avaliações, mensagens ou saldo.

Meus serviços lista somente anúncios pertencentes ao prestador, com pesquisa, filtro pelos estados reais do modelo, paginação e links para anúncios publicados. A modalidade não está modelada nos anúncios atuais e aparece como indisponível. A criação e edição completa não existem nesta versão; o botão de criar anúncio fica indisponível e sinaliza a Alpha 0.4.2. Não se inventa estado “em análise” para anúncios, pois o modelo não o possui.

Perfil profissional permite alterar nome público, descrição, foto e especialidades ativas; CPF/CNPJ, status, UUID e dados privados não pertencem ao formulário. A foto usa o validador de imagem, conferência do conteúdo JPEG/PNG/WebP, limite de 5 MB/20 MP, remoção de EXIF e re-encode para WebP. O perfil público aprovado continua acessível; a prévia autenticada também está disponível.

O portfólio aceita até 20 imagens JPG/PNG/WebP, de até 5 MB e 20 MP, reprocessadas para WebP. Os bytes ficam em storage privado cifrado, sem URL pública; leitura, exclusão e ordenação exigem o prestador proprietário aprovado. As imagens permanecem privadas até que exista fluxo de moderação/publicação. Associação a anúncios ainda não está disponível.

Onde atendo edita modalidades existentes, cidade/UF e região/raio aproximados usando a solicitação do próprio usuário; endereço residencial, ponto fixo e complemento não são exibidos nem alterados nessa tela. Mudanças de cidade/UF são refletidas no perfil público. Configurações mostram o estado geral da análise sem exibir, baixar ou editar documentos.

API autenticada para o futuro cliente móvel:

- `GET /api/v1/providers/me/dashboard/`: contagens reais de anúncios do prestador autenticado e `views_available=false`.
- `GET/PATCH /api/v1/providers/me/profile/`: consulta/edição limitada a nome público, descrição e especialidades; id/cidade/UF somente leitura. A autorização deriva de `request.user` e exige perfil aprovado.

A API não expõe documentos privados, portfólio ou dados de outros perfis. A gestão de anúncios, autenticação mobile, solicitações, mensagens, notificações, agenda, avaliações e financeiro continuam fora desta versão.

## Estado

O onboarding progressivo está implementado no app `apps.providers` e usa a conta BICO existente. O cadastro cria uma solicitação privada, não um segundo usuário nem um `ProviderProfile` público. O modo Prestador não é liberado automaticamente.

O CTA aparece na Home e em Minha Conta. Usuários anônimos passam pelo login com o destino de onboarding; rascunhos voltam à etapa salva e solicitações enviadas abrem a página de acompanhamento.

## Etapas

1. Tipo: profissional autônomo (PF) ou empresa (PJ).
2. Identificação, contato e documentos: dados pessoais ou empresariais e representante, com campos opcionais recolhidos. CPF/CNPJ têm dígitos verificadores; telefone e UF são validados no servidor. A escolha é RG, CIN ou CNH, com upload privado separado de frente/verso e substituição antes do envio. Na Web, continuar exige as duas fotos válidas; salvar e sair permite manter a etapa sem fotos.
3. Perfil e especialidades: nome público, descrição, experiência, categoria principal e categorias ativas. O limite de categorias usa `BICO_PROVIDER_MAX_CATEGORIES` (padrão 5). Não cria anúncio, preço, avaliação ou perfil público.
4. Atendimento: combina domicílio, ponto fixo e remoto em cards compactos. O CEP consulta ViaCEP e preenche rua, bairro, cidade/UF; há edição manual se não encontrar ou se o serviço falhar. Número/complemento ficam separados, raio usa slider e atendimento apenas remoto mostra cidade-base/UF. Um único par cidade/UF também preenche os campos internos do ponto fixo. O endereço fica privado, sem publicação automática, GPS ou distância calculada.
5. Revisão e envio: resumo editável por etapa, identificadores parcialmente mascarados, especialidades, modalidades, região e checklist dos documentos. A Web exige ciência de que o envio depende de análise e não libera publicação. Rascunhos antigos sem documentos podem enviá-los nesta etapa.

Os dados do rascunho são persistidos progressivamente no MySQL. Campos PF/PJ que não pertencem à modalidade escolhida não são aceitos pelo formulário daquela etapa.

A interface dedicada da Alpha 0.4.1 remove o cabeçalho/rodapé do marketplace somente neste fluxo. O salvamento automático reutiliza PATCH da API para etapas 1–4 válidas; entradas incompletas ou inválidas continuam sinalizadas como não salvas. Não guarda dados pessoais ou imagens em localStorage. O upload assíncrono usa o endpoint privado existente e o POST multipart continua funcionando sem JavaScript. Ver [experiência do onboarding](../04-interface/onboarding-prestador.md).

## Documentos e pré-validação

Cada solicitação admite uma imagem de frente e uma de verso. São aceitos somente conteúdos reais JPEG, PNG ou WebP, até 8 MB, até 25 megapixels e com dimensões mínimas de 800 × 500. O backend decodifica o arquivo, rejeita imagem corrompida ou grande demais e verifica heurísticas simples de escurecimento, falta de detalhes e desfoque. Imagens aprovadas pela pré-validação são reprocessadas para remover metadados EXIF.

PDF para documentos empresariais adicionais fica planejado para uma etapa futura, condicionado a processamento seguro. Não é aceito no upload atual de identidade e não substitui as fotografias de frente/verso de RG, CIN ou CNH. A opção “Tenho uma empresa ou MEI” mantém o tipo `COMPANY` e a identificação por CNPJ; não cria outra categoria de conta.

Na revisão, “salva para análise” significa somente que a imagem passou pela pré-validação técnica e foi armazenada. Fotos faltantes aparecem como “envio pendente”; uma foto que não passou pela pré-validação exige substituição. O cadastro continua rascunho até o envio, quando passa a aguardar verificação documental e aprovação humana.

Essa inspeção trata apenas formato e qualidade visual. Não usa OCR, não lê ou compara CPF, não reconhece rosto, não prova autenticidade, não consulta governo e não substitui a revisão humana. Nenhuma imagem recebe aprovação automática.

Os bytes são cifrados com Fernet antes de chegar ao filesystem privado. O nome original não é persistido; o caminho usa UUID e não possui URL pública. Uma rota autenticada pode transmitir a imagem somente ao proprietário, com `Cache-Control: private, no-store`, `nosniff` e política CSP restritiva. Os metadados dos documentos não aparecem no serializer do onboarding nem nos endpoints públicos.

## Envio e revisão

O serviço confirma campos obrigatórios, especialidades, modalidades e os dois documentos antes de alterar o estado. O envio é transacional e idempotente para uma solicitação já pendente. O estado resultante é `PENDING_REVIEW`; o campo interno de revisão fica `NOT_REVIEWED`, sem revisor, decisão ou motivo. A mensagem visível é **“Aguardando verificação documental e aprovação”**.

O modelo reserva estados `APPROVED` e `REJECTED`, motivo, revisor e data de revisão, mas não há tela ou endpoint de gestão. Os serializers não aceitam nem retornam esses campos internos. `NEEDS_CORRECTION` está reservado para uma futura operação autorizada; correções operacionais não são gerenciáveis por BICO Gestão nesta versão.

## Configuração e pendências de lançamento

Desenvolvimento habilita o onboarding para testes locais com dados sintéticos. Produção força `PROVIDER_ONBOARDING_ENABLED=False` e `PROVIDER_DOCUMENT_UPLOAD_ENABLED=False`, independentemente de variáveis de ambiente. Não abrir a coleta de documentos reais até aprovação jurídica e revisão de finalidade/base legal, aviso de privacidade, retenção e descarte, proteção do MySQL e backups, gestão/rotação de chaves, quarentena e operação de revisão. Os campos privados do rascunho ainda dependem dos controles de criptografia e backup do banco de produção; o armazenamento do arquivo de imagem, por sua vez, já cifra o conteúdo.

Não existe scanner antivírus configurado e, portanto, o sistema não declara arquivos livres de malware. E-mails, documentos empresariais adicionais, aceites de documentos jurídicos versionados e verificação de titularidade também não estão implementados.

## API autenticada

- `GET/PATCH /api/v1/providers/onboarding/`: consulta a solicitação do usuário da sessão e atualiza uma das etapas 1–4 por formulário de allowlist.
- `POST /api/v1/providers/onboarding/documents/`: recebe `side=FRONT|BACK` e `file` multipart, valida e substitui a imagem daquele lado.
- `POST /api/v1/providers/onboarding/submit/`: valida e envia a solicitação.

As rotas exigem autenticação. A Web e a API compartilham os mesmos forms e serviços de domínio; a API usa SessionAuthentication, portanto mutações por sessão exigem CSRF. Upload e envio usam throttling compartilhado no MySQL, com chave HMAC e limites de dez uploads e cinco envios por usuário/IP por hora. O UUID recebido não concede acesso a outra solicitação; o serviço sempre usa `request.user`.

## Próximas etapas

- **Alpha 0.4.2 — Publicação e gestão de anúncios:** criar, editar, enviar para revisão e gerenciar anúncios. O dashboard atual não oferece CRUD incompleto.
- **BICO Gestão — numeração a definir:** análise humana restrita, correções, histórico de decisões, retenção e gestão de acesso. Exige revisão jurídica e operacional antes de documentos reais.
- Antes de disponibilizar documentos reais: decisões jurídicas e de segurança indicadas acima, testes integrados em banco MySQL isolado e revisão de acessibilidade/responsividade.
