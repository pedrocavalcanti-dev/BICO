# Changelog

## 0.2.0-alpha — 2026-11-04

- Home de marketplace dirigida por MySQL, busca e páginas públicas de serviços e prestadores.
- Modelos/admin de banners, categorias, perfis de profissionais/empresas e anúncios de serviços.
- API pública de leitura paginada e serializers de campos públicos.
- Seed demonstrativo seguro para desenvolvimento, sem imagens externas nem avaliações inventadas.
- Fontes locais Inter e Quicksand, CSS responsivo, área geográfica apenas visual e documentação atualizada.
- 21 testes sem banco temporário; migrations aplicadas ao schema MySQL local existente.

## 0.1.1-alpha — 2026-11-04

- Decisão vigente de MySQL, backend Django e driver `mysqlclient`; servidor 8.0.46 validado e migrations aplicadas ao schema vazio `bico`.
- Tokens CSS, estilos base/componentes, integração das logos fornecidas e uso dos favicons existentes.
- Documentação atualizada para registrar a mudança desde PostgreSQL e preparar a futura Home de serviços.

## 0.1.0-alpha — 2026-11-04

- Inicialização do monorepositório Django e documentação arquitetural.
- Usuário customizado UUID/e-mail, apps iniciais, API v1 e Home mínima.
- PostgreSQL foi configurado, mas não estava disponível no ambiente local para migrations aplicadas.
