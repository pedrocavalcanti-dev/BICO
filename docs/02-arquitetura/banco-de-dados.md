# Banco de dados

MySQL 8.0.11 ou superior é obrigatório para desenvolvimento integrado e produção. A configuração usa `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` e `DB_PORT`, carregadas do ambiente e do `.env` na raiz do monorepo. `DB_ENGINE` deve ser `mysql`; configurações de outros backends são rejeitadas.

O driver único é `mysqlclient`. A conexão solicita `utf8mb4`, modo SQL estrito, isolamento `READ COMMITTED` e InnoDB para tabelas criadas pela conexão. Essas opções são por conexão/sessão; não alteram configurações globais do servidor. O banco existente deve usar `utf8mb4` e InnoDB; inspecione charset, collation, engines, tabelas e privilégios antes de migrar.

Não existe fallback para PostgreSQL ou SQLite. As credenciais locais não são versionadas. Produção exige usuário de aplicação com privilégios mínimos; não usar root.

Usuários, perfis profissionais, categorias, anúncios e banners usam UUID. `ProviderProfile` se relaciona 1:1 com `accounts.User`; perfis ligam-se a categorias em N:N; `ServiceListing` referencia um prestador e uma categoria; `HomeBanner` é independente. Índices cobrem status/destaque/data de publicação, status/categoria/data e status/cidade/data.

Na Alpha 0.3.1, `ServiceListingImage` adiciona uma galeria 1:N para anúncios, com imagem, texto alternativo, ordem e data de criação. A ordem é única por anúncio. A migration `catalog.0003_servicelistingimage` cria somente a nova tabela; aplique-a em MySQL antes de executar o seed atualizado.

Anúncios públicos exigem status `PUBLISHED`, perfil `APPROVED` e categoria ativa. Perfis públicos exigem `APPROVED`. Fotos são opcionais; Django `ImageField` valida a imagem e um validador limita extensões a JPG/PNG/WebP e tamanho a 5 MB. Upload em produção requer decidir storage e política de retenção. Avaliações e distância ainda não têm modelo.

`seed_bico_demo` só roda com `DEBUG=True` e backend MySQL. Seus perfis, anúncios e banners têm `is_demo=True`; o comando não apaga dados e não altera linhas legítimas. Ele copia imagens WebP locais para campos ainda vazios nos registros demonstrativos e nas capas de categoria. A tabela de usuários também recebe contas demonstrativas com senha inutilizável. As imagens de `static/marketplace/demo/` são assets de origem para o seed, não storage definitivo de uploads; em produção deve ser escolhido um backend de mídia apropriado.
