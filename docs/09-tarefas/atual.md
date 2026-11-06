# Tarefa atual — Alpha 0.3.2: imagens e refinamento visual

- [x] Inspecionar instruções, estado da Alpha 0.3.1, documentação do marketplace, seed, modelos, admin e páginas públicas.
- [x] Criar `feature/bico-alpha-0.3.2-visual-assets` a partir da Alpha 0.3.1, preservando o histórico e a Home Alpha 0.2.0.
- [x] Gerar e otimizar 81 assets WebP locais distintos: 60 fotos de trabalho, seis imagens de anúncio, 12 retratos e três logos.
- [x] Completar capa e galerias distintas dos 36 anúncios demo; cobrir as 12 categorias e os 18 perfis demo.
- [x] Corrigir especialidades, apresentações e associações demonstrativas sem alterar perfis ou anúncios reais.
- [x] Reorganizar perfil público, cards de anúncio, portfólio, perfis relacionados e recorte de logos; manter a Home e os banners sem redesign.
- [x] Exigir duas imagens distintas no admin ao publicar anúncios novos; manter rascunhos sem fotos e permitir editar anúncios já publicados.
- [x] Tornar o seed idempotente para arquivos com sufixo de colisão gerado pelo armazenamento, preservando arquivos personalizados.
- [x] Documentar origem e uso dos assets, seed, páginas, regra de publicação, estado, roadmap e release.
- [x] Executar o seed no MySQL local com `DEBUG=True`; verificações confirmaram 36 capas únicas, 41 fotos de galeria, 12 categorias com imagem e 18 perfis com avatar/logo. Repetições não criaram registros nem trocaram os nomes de arquivos já semeados.
- [x] Validar `manage.py check`, `makemigrations --check --dry-run`, 25 testes focados de `apps.catalog.tests` e `apps.core.tests`, Ruff nos módulos Python alterados e integridade/formato dos 81 assets.
- [x] Confirmar que `.env`, logs, banco local, caches e temporários permanecem ignorados pelo Git.
- [x] Revisar Home, anúncio e perfil em navegador com viewport mobile de 412 px e desktop de 1440 px. A página não excede a largura do viewport; composição mobile e desktop conferidas.
- [x] Revisar o diff, confirmar que arquivos sensíveis e locais estão ignorados e preparar o commit final local para publicação sem force push.

Limites mantidos: sem migrations, alteração de contratos API, contratação, chat real, avaliações, pagamento ou modo Prestador. A suíte completa continua pendente porque o usuário MySQL de aplicação não pode criar `test_bico` (erro 1044); não usar o schema principal como substituto. A branch não será integrada à `main` nesta entrega.
