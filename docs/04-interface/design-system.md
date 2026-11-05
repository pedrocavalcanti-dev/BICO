# Design System BICO — fundação

O design system usa tokens, estilos de base e componentes compartilhados da Home, busca, detalhe de serviço e perfil público. Ações comerciais e autenticação ainda não estão implementadas.

## CSS

Os arquivos são carregados pelo template base via Django Static Files:

- `static/css/tokens.css`: cores, tipografia, escala de espaçamento, raios, sombra, alturas e medidas de layout.
- `static/css/base.css`: reset leve, tipografia sem dependência remota, imagens, elementos semânticos, foco e preferência por movimento reduzido.
- `static/css/components.css`: container, botões, campos, cards, badges, alertas, estado vazio, skeleton de referência e cabeçalho de seção.
- `static/css/site.css`: cabeçalho, navegação, footer e estilos compartilhados das páginas públicas.
- `static/css/home.css`: banner, rails de conteúdo, cards de categoria, chamada de cadastro e área reservada do futuro mapa.
- `static/fonts/`: Inter variável e Quicksand 700 com licenças OFL; nenhuma fonte remota.

HTML usa classes pequenas e sem dependências JavaScript. Só usar controles interativos quando houver ação real; estilos de estado disabled não simulam uma ação existente.

## Tokens e componentes

Os tokens oficiais e usos estão em [identidade-visual.md](identidade-visual.md). Consultar `:root` em `tokens.css` antes de introduzir valores visuais. Quicksand Bold é usada em títulos; Inter cobre interface, textos e pesos de 400 a 700. Cor de títulos: `#253D4E`; menu: 13 px / 24 px; títulos de seção: 24 px / 28,8 px em telas largas.

Os componentes disponíveis são classes de apresentação, não componentes JavaScript. Formularios devem manter `<label>` associado ao campo e erros textuais; links continuam links e botões executam ações. `:focus-visible` é mantido no CSS base, e `prefers-reduced-motion` reduz transições/animações.

## Layout e responsividade

O container usa largura máxima centralizada e gutters fluidos. Títulos usam `clamp()` para escalonar sem muitos breakpoints. A página ajusta header, coluna de conteúdo, card informativo e footer em telas menores (`40rem`). Adicionar novos breakpoints apenas quando o conteúdo exigir.

## Sequência planejada da Home

1. Header laranja com marca, busca de serviço/profissional e filtro de cidade.
2. Navegação horizontal por categorias ativas do banco.
3. Carrossel responsivo de banners ativos, com fallback visual local.
4. Profissionais autônomos em destaque e categorias editoriais.
5. Chamada para prestadores, com destino informativo enquanto cadastro não existe.
6. Área reservada à futura descoberta geográfica, sem mapa ou coordenadas falsos.
7. Anúncios destacados, outros anúncios e empresas aprovadas.
8. Anúncios recentes, especialidades e footer institucional.

Os dados comerciais são consultados do MySQL por seletores compartilhados pela Web e API. Não fixar conteúdo de anúncios nos templates. O seed local é identificável como demonstração. A área geográfica é somente composição visual: sem mapa, geolocalização, distância ou coordenadas nesta etapa.
