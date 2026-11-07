# ADR-011 — Preenchimento de endereço por CEP

- **Status:** Aceita para a UX local do onboarding; coleta de produção continua desativada
- **Data:** 2026-11-06

## Contexto

A Alpha 0.4.1 exige reduzir digitação de endereço sem implementar mapas ou contratar um serviço de localização. O banco existente já possui os campos privados de ponto de atendimento; não é necessário criar outro cadastro ou mudar o schema.

## Decisão

Consultar o [webservice oficial ViaCEP](https://viacep.com.br/) diretamente no navegador com HTTPS e CEP de oito dígitos. Enviar apenas o CEP, com `credentials: omit` e `referrerPolicy: no-referrer`; não enviar CPF, documento, nome, número, complemento ou credenciais da conta. O serviço também recebe os dados de conexão próprios de uma requisição de navegador, como IP e origem.

Usar JSON, verificar HTTP/indicador de erro e aplicar timeout. Sem resultado, sem JavaScript ou sem disponibilidade do serviço, permitir digitação manual. Não persistir respostas em localStorage e não usar o resultado como verificação de identidade, residência ou titularidade.

A cidade/UF única da interface preenche os campos internos existentes quando o ponto fixo não fornece valores próprios. Os mesmos forms continuam responsáveis por normalização e validação no backend. A classificação visual das especialidades não altera a taxonomia do catálogo.

## Consequências

Há uma dependência externa opcional para conveniência de preenchimento, solicitada para esta experiência, sem chave, SDK ou serviço de hospedagem novo. Indisponibilidade não impede cadastro manual. Nenhuma alteração de modelo, migration ou endpoint público é necessária. Os controles jurídicos e de segurança da coleta de produção continuam pendentes conforme ADR-010.
