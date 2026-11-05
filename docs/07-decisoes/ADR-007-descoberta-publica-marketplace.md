# ADR-007 — Leitura pública do marketplace

- **Estado:** aceito
- **Data:** 2026-11-04
- **Contexto:** A Home precisa de dados de MySQL e os aplicativos futuros devem consumir os mesmos dados. Os fluxos de cadastro, contratação, avaliações e localização ainda não estão definidos.

## Decisão

- Manter `catalog` para categorias/anúncios e `providers` para perfis individuais e de empresas; `core` mantém banners e composição da Home.
- Centralizar regras de publicação em seletores reutilizados pela Web e API. Só perfis aprovados, anúncios publicados e categorias ativas são públicos.
- Expor leitura pública por serializers explícitos, `AllowAny`, métodos `GET`/`HEAD`, paginação de no máximo 48 por página e filtros limitados.
- Marcar dados de demonstração explicitamente; permitir o seed apenas em `DEBUG=True` com MySQL.
- Reservar o bloco geográfico sem coletar localização nem simular mapa, pontos ou distâncias.

## Consequências

O catálogo pode ser explorado antes de implementar autenticação. A criação/edição de conteúdo permanece restrita ao Django Admin técnico nesta etapa. A API não oferece operações de escrita. Avaliações, disponibilidade, contratação e busca geográfica exigem regras e modelos próprios antes de aparecerem publicamente.
