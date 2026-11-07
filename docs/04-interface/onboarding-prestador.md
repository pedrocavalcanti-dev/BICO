# Experiência do onboarding profissional — Alpha 0.4.1

O fluxo usa uma tela dedicada e a conta BICO existente. `providers/base_onboarding.html` reaproveita o documento HTML e os tokens globais, substituindo apenas o cabeçalho/rodapé do marketplace por navegação própria. O desktop apresenta trilha lateral; no mobile, logo, salvar/sair e uma barra compacta de progresso priorizam o formulário. Não há altura fixa nos formulários.

## Etapas e componentes

1. **Seu caminho:** duas escolhas PF/PJ com ícone, descrição curta e seleção visível. A opção vazia do widget foi removida.
2. **Identificação:** dados essenciais em grade, detalhes opcionais em acordeão, escolha de RG/CIN/CNH e duas fotos privadas. A empresa mantém os campos necessários do responsável. O upload permite escolher/arrastar, visualizar e substituir a foto, com validação por imagem e confirmação somente depois da persistência no servidor.
3. **Perfil:** nome, apresentação com contador e experiência opcional recolhida. Especialidades ativas são agrupadas visualmente por área, com ícones SVG locais, busca sem distinção de acentos, seleção compacta e limite configurável. A categoria principal precisa estar selecionada.
4. **Atendimento:** modalidades combináveis. CEP como entrada principal, resultado compacto, número/complemento separados e editor manual. O atendimento somente remoto mostra cidade-base/UF e abrangência. O slider representa o raio informado, sem localização calculada ou mapa.
5. **Revisão:** cards com links de edição, identificadores mascarados, especialidades, modalidades, região e estado dos documentos. Ciência explícita de que é necessário aguardar aprovação; não constitui aceite jurídico versionado. Documentos pendentes de rascunhos antigos podem ser completados nesta tela.

O sucesso apresenta recebimento, análise pendente e próximos passos. A previsão de até 24h é variável; não há promessa de aprovação, notificação automática ou operação de BICO Gestão implementada.

## Correções finais na branch Alpha 0.4.0

O Enter na busca de especialidades apenas reaplica o filtro, sem submeter o formulário. A causa era o envio implícito acionar o primeiro submit associado ao formulário, “Salvar e sair”, mesmo estando no cabeçalho. Os botões já tinham `type` explícito; o tratamento foi limitado ao campo de busca e respeita a composição de texto. Enter em textarea e nos botões continua funcionando.

A escolha PJ agora se apresenta como “Tenho uma empresa ou MEI”, com o mesmo valor `COMPANY` e fluxo CNPJ. A revisão identifica o cadastro como rascunho e as fotos como salvas para análise, sem afirmar aprovação. PDF empresarial permanece planejado e desabilitado. O layout foi preservado.

## Feedback e acessibilidade

- Inter e Quicksand locais e laranja dos tokens oficiais. Ícones vetoriais originais feitos em código, sem download ou biblioteca visual adicional.
- Inputs com labels, foco visível, mensagens por campo e abertura dos acordeões que contêm erros. Seleções mantêm radios/checkboxes nativos e navegação por teclado.
- Transições leves em cards e entrada de página; `prefers-reduced-motion` desativa animações.
- Salvamento automático serializado nas etapas 1–4 após a validação dos campos. O texto “Salvo automaticamente” só aparece após HTTP de sucesso da API; campos incompletos/invalidáveis permanecem “Alterações não salvas”. O backend conserva a validação completa da etapa.
- Upload possui estados de envio, sucesso e erro. Os botões de continuar/sair aguardam o envio. A senha de sessão e os arquivos não são gravados em localStorage; prévias temporárias ficam somente em memória.
- Sem JavaScript, o POST multipart e as validações do servidor continuam disponíveis. O CEP pode ser preenchido manualmente e os opcionais usam `<details>` nativo.

## Localização

ViaCEP é consultado por HTTPS somente com o CEP de oito dígitos, sem cookies ou referrer da BICO. Há timeout, tratamento de CEP inexistente e fallback manual. A consulta ajuda o preenchimento; o servidor continua validando os campos e a UF. A integração e suas limitações estão no [ADR-011](../07-decisoes/ADR-011-preenchimento-por-cep.md).

## Validação

Layout verificado em Edge headless em 360, 390, 768, 1024 e 1440 px. Capturas e relatórios locais com dados sintéticos ficam em `artifacts/onboarding-ux/`, ignorado pelo Git. Interações do navegador usam respostas de rede controladas para exercitar a UI sem dados reais; persistência, autorização, upload e envio pendente são conferidos separadamente no MySQL em transação revertida. Isso não substitui a suíte integral em banco de teste nem uma auditoria completa de acessibilidade.
