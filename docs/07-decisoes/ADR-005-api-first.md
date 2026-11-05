# ADR-005 — API First

- **Estado:** aceito.
- **Contexto:** site/PWA será acompanhado por Flutter Android/iOS.
- **Decisão:** manter API REST versionada e regras críticas no backend; Web e mobile compartilham serviços do domínio.
- **Consequência:** API não pode depender de estado exclusivo do template. Transporte de autenticação mobile será decidido antes dessa integração.
