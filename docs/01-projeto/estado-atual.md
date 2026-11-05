# Estado atual

**Versão:** 0.2.0-alpha

**Atualizado:** 2026-11-04

**Ambiente inspecionado:** Windows, PowerShell, Python 3.12.10, Django 5.2.19, DRF 3.18.3, MySQL Server 8.0.46

## Implementado nesta etapa

- Home de marketplace responsiva na ordem visual aprovada: header/busca, categorias, banners, profissionais, serviços em destaque, chamada para prestadores, área reservada a mapa, anúncios, empresas, novidades, especialidades e footer.
- Fontes locais Inter variável e Quicksand 700; tokens de pesos, famílias, tamanhos e cores atualizados para as referências tipográficas fornecidas.
- Apps `providers` e `catalog`; modelos `ProviderProfile`, `ServiceCategory`, `ServiceListing` e `HomeBanner`, com UUID, relações, estados de publicação, datas, índices e campos demonstrativos.
- Seletores compartilhados entre a Home/API, restringindo perfis a `APPROVED` e anúncios a `PUBLISHED` com categoria ativa.
- Busca Web por título, categoria, prestador e cidade; páginas simples de resultados, anúncio e perfil; destinos informativos para ações futuras.
- API v1 pública de leitura para Home, categorias, perfis e anúncios; paginação limitada e serializers sem dados privados.
- Admin técnico dos quatro modelos e comando MySQL/DEBUG `seed_bico_demo`, idempotente e sem remoção ou alteração de registros legítimos.
- Fallbacks CSS locais quando banners, capas, avatars ou imagens de anúncio não estão disponíveis. Nenhuma imagem externa é carregada.
- Área de proximidade sem mapa, geolocalização, distância ou pins falsos.

## Validado neste ambiente

- `manage.py check`: sem erros.
- `makemigrations --check --dry-run`: nenhuma migration pendente após gerar as migrations versionadas.
- `manage.py migrate --noinput`: aplicou apenas as novas tabelas e índices `catalog`, `providers` e `core` no MySQL local existente; não criou nem apagou o schema.
- `manage.py test`: 21 testes passaram. São testes unitários/web/API sem criação de banco temporário.
- Seed inicial criou 12 categorias, 18 perfis demonstrativos, 36 anúncios e 3 banners. Reexecuções não criaram duplicatas; os 36 títulos demonstrativos são distintos.
- Cliente Django contra o banco local: `/`, `/servicos/`, busca filtrada, endpoints raiz/health/Home/categorias/perfis/anúncios responderam 200.
- Testes confirmaram `POST`, `PUT`, `DELETE` e `OPTIONS` recusados em listagens públicas e parâmetros de busca fora do limite retornando 400.
- `findstatic` localizou `css/home.css`, `js/home.js` e a fonte Inter vendorizada.
- Página inteira conferida no Edge em 360, 390, 768, 1024 e 1440 px, sem overflow horizontal do documento; capturas locais estão em `artifacts/responsive-alpha-0.2.0/` e são ignoradas pelo Git.

## Regras e limites

- O estado aprovado de perfil e publicado de anúncio controla a descoberta pública. E-mail, usuário, estado de moderação e dados documentais não fazem parte dos serializers públicos.
- Conteúdo demonstrativo tem `is_demo=True`, senha inutilizável e identificação visual na Home. Ele existe apenas no MySQL de desenvolvimento; o comando falha fora de `DEBUG=True` e MySQL.
- Não há avaliações, preço presumido, distância, localização precisa ou status de verificação inventados. Anúncios demonstrativos podem mostrar preço ou “Sob orçamento” porque isso está explicitamente marcado como demonstração.
- Cadastro/login, solicitação/contratação, chat, notificações funcionais, favoritos persistentes, avaliações, mapa real e pagamentos permanecem pendentes.
- Fotos e banners oficiais ainda não foram recebidos; a interface usa fallback CSS até existirem imagens autorizadas. O Figma editável não está no repositório, então a composição segue as referências visuais compartilhadas.

## Próximos passos

Implementar autenticação/cadastro e habilitação de perfil profissional com regras de aprovação; depois, solicitações de serviços. Planejar armazenamento definitivo de mídia e mapa somente com requisitos e dados adequados.
