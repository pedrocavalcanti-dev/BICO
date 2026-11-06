# Onboarding do prestador — Alpha 0.4.0

## Estado

O onboarding progressivo está implementado no app `apps.providers` e usa a conta BICO existente. O cadastro cria uma solicitação privada, não um segundo usuário nem um `ProviderProfile` público. O modo Prestador não é liberado automaticamente.

O CTA aparece na Home e em Minha Conta. Usuários anônimos passam pelo login com o destino de onboarding; rascunhos voltam à etapa salva e solicitações enviadas abrem a página de acompanhamento.

## Etapas

1. Tipo: profissional autônomo (PF) ou empresa (PJ).
2. Identificação e contato: dados pessoais ou empresariais e representante. CPF/CNPJ têm dígitos verificadores; telefone e UF são validados no servidor. A escolha de documento é RG, CIN ou CNH.
3. Perfil e especialidades: nome público, descrição, experiência, categoria principal e categorias ativas. O limite de categorias usa `BICO_PROVIDER_MAX_CATEGORIES` (padrão 5). Não cria anúncio, preço, avaliação ou perfil público.
4. Atendimento: combina domicílio, ponto fixo e remoto. A cidade/UF e os dados exigidos por modalidade são validados no backend. Endereço fixo fica privado, sem publicação automática, GPS ou distância calculada.
5. Revisão e documentos: resumo com identificadores parcialmente mascarados; upload separado de frente e verso; arquivos podem ser substituídos antes do envio. O formulário mostra instruções, prévia e mensagens para cada problema de qualidade.

Os dados do rascunho são persistidos progressivamente no MySQL. Campos PF/PJ que não pertencem à modalidade escolhida não são aceitos pelo formulário daquela etapa.

## Documentos e pré-validação

Cada solicitação admite uma imagem de frente e uma de verso. São aceitos somente conteúdos reais JPEG, PNG ou WebP, até 8 MB, até 25 megapixels e com dimensões mínimas de 800 × 500. O backend decodifica o arquivo, rejeita imagem corrompida ou grande demais e verifica heurísticas simples de escurecimento, falta de detalhes e desfoque. Imagens aprovadas pela pré-validação são reprocessadas para remover metadados EXIF.

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

- Alpha 0.4.1: operação restrita de análise, correções, histórico de decisões, retenção e gestão de acesso.
- Alpha 0.4.2: perfil público e publicação de anúncios pelo prestador após aprovação.
- Antes de disponibilizar documentos reais: decisões jurídicas e de segurança indicadas acima, testes integrados em banco MySQL isolado e revisão de acessibilidade/responsividade.
