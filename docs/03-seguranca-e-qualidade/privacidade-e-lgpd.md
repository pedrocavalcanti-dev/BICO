# Privacidade e LGPD

Na UX Alpha 0.4.1, o preenchimento opcional por ViaCEP envia somente CEP ao serviço, sem cookies BICO ou referrer; número/complemento, identificação e imagens não integram essa consulta. O serviço recebe metadados de conexão próprios da requisição. Há alternativa manual e nenhum resultado é usado como prova de residência ou identidade. Ver ADR-011. A ciência da revisão final não equivale a um aceite jurídico versionado; a coleta real de produção continua bloqueada.

Coletar apenas dados necessários para a finalidade do serviço, com controle de acesso, retenção e exclusão definidos antes de cada funcionalidade. Não exigir CPF nesta fundação. Região de atendimento pode ser pública; endereço residencial preciso não deve ser exposto sem necessidade legítima.

Logs e auditoria devem evitar tokens, senhas, conteúdo de conversa e payloads pessoais. Processos de atendimento a titulares, base legal, prazos de retenção e política pública de privacidade ainda precisam de definição antes do lançamento com usuários reais.

## Onboarding profissional — Alpha 0.4.0

O rascunho contém CPF/CNPJ, data de nascimento, contatos empresariais, dados de representante e endereço de ponto fixo. Esses campos não aparecem em páginas públicas; somente a pessoa proprietária recebe seus dados por sessão/API autenticada. Fotos de documento são cifradas no storage privado e servidas sem cache somente ao proprietário. Registros de auditoria guardam apenas o tipo de evento e, no upload, o lado da imagem.

A configuração de produção mantém onboarding e envio de documentos desativados. Antes de habilitar coleta real, definir e aprovar finalidade/base legal, minimização por PF/PJ, aviso de privacidade, prazo de retenção e descarte verificável, processo de acesso da equipe revisora, tratamento de incidentes, proteção do MySQL/backups e gestão/rotação/recuperação das chaves Fernet. A cifragem dos arquivos não substitui proteção dos campos no banco nem de cópias de segurança. Usar somente dados sintéticos em desenvolvimento.
