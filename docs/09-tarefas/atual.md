# Tarefa atual

## Alpha 0.2.0 — Home Marketplace BICO

- [x] Ler escopo, documentação, estado Git e estrutura existente.
- [x] Criar branch local `feature/bico-alpha-0.2.0-home` sem alterar `main`.
- [x] Implementar modelos e migrations de categorias, prestadores, anúncios e banners.
- [x] Implementar seletores públicos, Home, busca, páginas simples de perfil/anúncio e páginas informativas.
- [x] Implementar API de leitura com paginação, limites, filtros e bloqueio de métodos de escrita.
- [x] Integrar fontes locais Inter e Quicksand, componentes reutilizáveis, CSS/JS responsivos e marca oficial.
- [x] Implementar seed de demonstração protegido por `DEBUG=True` e MySQL; executar e confirmar repetição sem duplicação.
- [x] Atualizar documentação de arquitetura, dados, API, interface, roadmap e release.
- [x] Executar `check`, `makemigrations --check --dry-run`, 21 testes, migrations, cliente Django e `findstatic`.
- [x] Revisar a interface em viewport de navegador 360, 390, 768, 1024 e 1440 px; confirmar ausência de overflow horizontal da página.
- [x] Registrar capturas de página inteira em `artifacts/responsive-alpha-0.2.0/home-{360,390,768,1024,1440}.png` (arquivos locais ignorados pelo Git).
- [x] Revisar o diff final e criar commit local `feat: implement BICO marketplace homepage`.

Limites atuais: não há login/cadastro público, contratação, chat, avaliações, notificações funcionais ou mapa real. Banners e fotografias autorizadas continuam pendentes; a Home possui fallbacks CSS locais.
