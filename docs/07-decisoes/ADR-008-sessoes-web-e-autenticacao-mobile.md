# ADR-008 — Sessões Web e estratégia futura para autenticação mobile

- **Estado:** sessões Web implementadas; estratégia mobile registrada para decisão de implementação futura.
- **Data:** 2026-11-05.

## Contexto

A BICO precisa de login/cadastro Web agora e terá clientes Flutter mais adiante. Sessões Web, autenticação móvel e autorização de prestador atendem contextos diferentes. Usar JWT no navegador ou criar uma segunda conta aumentaria o risco e duplicaria identidade.

## Decisão para Web

Usar `django.contrib.auth` com sessão, cookies `HttpOnly`/`SameSite`, CSRF e `Secure` em produção. O logout exige POST. O usuário deriva da sessão nas views e APIs privadas. Endpoints autenticados com sessão continuam protegidos por CSRF.

## Direção para mobile (não implementada)

Ao iniciar o app Flutter, avaliar tokens de acesso de curta duração e tokens de renovação rotativos, vinculados a sessões/dispositivos. A renovação deve revogar a credencial anterior, detectar reutilização e permitir revogação por dispositivo e global. O app deve guardar segredos em Keychain (iOS) ou Android Keystore por meio de armazenamento seguro suportado pela plataforma; nunca em preferências sem proteção ou logs. Definir expiração, rotação, revogação, recuperação e respostas de erro em ADR de implementação antes de expor endpoints.

Não adotar JWT ou refresh tokens nesta Alpha. O contrato futuro permanece versionado em `/api/v1/`; cadastro, login e renovação mobile ainda não existem.

## Consequências

- A identidade única continua sendo `accounts.User` e as regras de perfil são compartilháveis.
- A API Web atual autentica por sessão e requer CSRF em mutações.
- A implementação mobile poderá introduzir tokens sem alterar o modelo de usuário nem abrir autenticação social fictícia.
