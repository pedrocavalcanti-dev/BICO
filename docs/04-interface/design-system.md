# Design System BICO — fundação

O design system nesta etapa define tokens, estilos de base e componentes CSS pequenos usados como referência para as próximas páginas. A Home continua sendo a página de fundação; catálogo, navegação completa e ações comerciais não estão implementados.

## CSS

Os arquivos são carregados pelo template base via Django Static Files:

- `static/css/tokens.css`: cores, tipografia, escala de espaçamento, raios, sombra, alturas e medidas de layout.
- `static/css/base.css`: reset leve, tipografia sem dependência remota, imagens, elementos semânticos, foco e preferência por movimento reduzido.
- `static/css/components.css`: container, botões, campos, cards, badges, alertas, estado vazio, skeleton de referência e cabeçalho de seção.
- `static/css/site.css`: composição da Home mínima e responsividade específica da página.

HTML usa classes pequenas e sem dependências JavaScript. Só usar controles interativos quando houver ação real; estilos de estado disabled não simulam uma ação existente.

## Tokens e componentes

Os tokens oficiais e usos estão em [identidade-visual.md](identidade-visual.md). Consultar `:root` em `tokens.css` antes de introduzir valores visuais. A paleta é laranja, branca e grafite/azul-acinzentado; superfícies e bordas usam cinzas neutros.

Os componentes disponíveis são classes de apresentação, não componentes JavaScript. Formularios devem manter `<label>` associado ao campo e erros textuais; links continuam links e botões executam ações. `:focus-visible` é mantido no CSS base, e `prefers-reduced-motion` reduz transições/animações.

## Layout e responsividade

O container usa largura máxima centralizada e gutters fluidos. Títulos usam `clamp()` para escalonar sem muitos breakpoints. A página ajusta header, coluna de conteúdo, card informativo e footer em telas menores (`40rem`). Adicionar novos breakpoints apenas quando o conteúdo exigir.

## Sequência planejada da Home

1. Header laranja com marca, busca e localização.
2. Navegação por categorias.
3. Banner(s) oficiais responsivos.
4. Profissionais populares e serviços mais procurados.
5. Chamada para cadastro de prestador.
6. Área reservada a profissionais próximos/mapa.
7. Serviços, anúncios e empresas prestadoras.
8. Anúncios recentes, categorias adicionais e footer institucional.

Os dados comerciais devem vir do Django quando os domínios forem implementados. Não fixar nomes, preços, avaliações, disponibilidade ou portfólio fictícios nos templates. A área de mapa é somente uma decisão de composição futura: sem mapa, geolocalização ou coordenadas nesta etapa.
