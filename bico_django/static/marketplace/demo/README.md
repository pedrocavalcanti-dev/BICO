# Imagens demonstrativas do marketplace

Este diretório reúne fotografias e identidades visuais usadas apenas em conteúdo demonstrativo. Os arquivos não representam clientes, prestadores, serviços contratados, avaliações ou empresas reais. Os assets oficiais BICO continuam exclusivamente em `static/branding/`.

## Origem e preparação

Os 81 novos arquivos Alpha 0.3.2 foram gerados para demonstração com OpenAI ImageGen, sem download ou hotlink de bancos de fotos externos. Quinze composições de trabalhos foram recortadas em quatro fotografias cada; os recortes, retratos e logos foram otimizados localmente em WebP. Nenhuma marca real foi usada nos logos fictícios. A ferramenta de geração é a origem do conteúdo; não há URL ou licença de terceiro a atribuir.

Os assets novos somam 4.303.738 bytes (aprox. 4,1 MiB); todos os 81 foram inspecionados como WebP legíveis, com hashes distintos e menos de 500 KB por arquivo. Os originais gerados ficaram fora do repositório; os arquivos abaixo são as versões WebP prontas para servir.

## Assets preexistentes

| Arquivo | Uso demonstrativo |
|---|---|
| `garden-trimmer.webp` | Jardinagem, capa de anúncio e banner |
| `lawn-mowing.webp` | Galeria de jardinagem |
| `garden-hedge-pruning.webp` | Categoria e galeria de jardinagem |
| `garden-planting.webp` | Galeria de jardinagem |
| `computer-repair.webp` | Tecnologia e banner |
| `wall-painting.webp` | Pintura e banner |
| `plumbing-repair.webp` | Encanamento |
| `home-cleaning.webp` | Limpeza |
| `electrical-installation.webp` | Elétrica |
| `automotive-diagnostics.webp` | Mecânica |
| `event-photography.webp` | Fotografia |
| `demo-provider-alex.webp` | Perfil fictício Alex Silva |
| `demo-provider-beatriz.webp` | Perfil fictício Beatriz Costa |
| `demo-provider-caio.webp` | Perfil fictício Caio Mendes |

## Assets adicionados na Alpha 0.3.2

| Grupo | Arquivos | Uso |
|---|---|---|
| Fotografias de trabalho | `sheet-01-1.webp` a `sheet-15-4.webp` (60 arquivos) | Capas e galerias de anúncios demo; cada arquivo é uma foto individual recortada, não uma folha de contato |
| Capas e fotos avulsas | `listing-06-cover.webp`, `listing-06-gallery.webp`, `listing-09-cover.webp`, `listing-09-gallery.webp`, `listing-11-cover.webp`, `listing-11-gallery.webp` | Pequenos reparos, montagem de móveis e design; também cobrem suas categorias |
| Retratos gerados | `demo-provider-04.webp` a `demo-provider-15.webp` (12 arquivos) | Perfis demonstrativos de Dani Ribeiro a Otávio Freire |
| Logos fictícios | `demo-company-equipe-verde.webp`, `demo-company-casa-em-ordem.webp`, `demo-company-oficina-horizonte.webp` | Perfis demonstrativos das três empresas do seed |

O manifesto de associação entre arquivo e registro está em `apps/catalog/management/commands/seed_bico_demo.py`. No MySQL local validado, os 36 anúncios publicados possuem capa e ao menos uma foto de galeria com arquivos distintos, as 12 categorias têm imagem e os 18 perfis demo têm retrato ou logo. O seed preserva mídia personalizada e dados reais; pode substituir apenas nomes de imagens demonstrativas explicitamente permitidos no manifesto, inclusive o sufixo aleatório de sete caracteres gerado pelo storage Django.

`seed_bico_demo` só executa com `DEBUG=True` e MySQL. Ele copia os arquivos para `MEDIA_ROOT`; `static/` não é storage para uploads de usuários. O armazenamento definitivo de uploads em produção permanece pendente.
