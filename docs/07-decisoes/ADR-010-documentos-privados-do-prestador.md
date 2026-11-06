# ADR-010 — Armazenamento privado de documentos do prestador

- **Status:** Aceita para desenvolvimento local; produção bloqueada por configuração
- **Data:** 2026-11-06

## Contexto

O onboarding do prestador exige imagens de identidade para análise humana. Esses arquivos contêm dados pessoais e não podem integrar os assets estáticos, URLs públicas ou respostas da API pública.

## Decisão

- Guardar somente JPEG, PNG e WebP validados por decodificação, com limite de tamanho/resolução e pré-validação visual simples. Reprocessar imagens e remover metadados EXIF.
- Cifrar os bytes com Fernet antes do filesystem privado. O storage não fornece URL; caminhos internos são aleatórios. Leitura ocorre por uma view autenticada vinculada ao proprietário e sem cache.
- Em desenvolvimento local, derivar uma chave do `DJANGO_SECRET_KEY` somente para dados sintéticos. Produção exige chaves Fernet externas (`BICO_PROVIDER_DOCUMENT_ENCRYPTION_KEYS`), mas mantém onboarding e upload forçados a desabilitados até existir aprovação jurídica e operacional. Configurar e testar `MultiFernet` com chave nova primeiro e chaves antigas depois para rotação.
- Não afirmar OCR, autenticidade, titularidade, correspondência do CPF ou análise antivírus. Apenas a equipe autorizada poderá fazer a revisão humana em uma etapa futura.
- Proteger dados pessoais em MySQL e backups no ambiente de infraestrutura; essa proteção ainda precisa de decisão e validação antes da coleta real.

## Consequências

Arquivos armazenados não são imagens JPEG/PNG/WebP legíveis diretamente no disco: o storage descriptografa apenas após autorização do servidor. Perder todas as chaves torna os arquivos irrecuperáveis; cópias de segurança e rotação precisam ser operadas com controle. O armazenamento atual é local e privado, não uma decisão de storage escalável para produção. A coleta real continua fechada.

## Alternativas

- `static/` ou mídia com URL pública: rejeitado por expor documentos.
- Confiança em extensão e Content-Type enviados pelo navegador: rejeitada por não validar o formato real.
- OCR ou KYC externo: fora do escopo desta versão e sem base jurídica/integração aprovada.
