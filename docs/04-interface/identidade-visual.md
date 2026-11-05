# Identidade visual BICO

## Marca

Os dois arquivos oficiais fornecidos estão em `bico_django/static/branding/logos/`:

- `logo-bico-sem-fundo.png`: versão clara/transparente para fundos laranja.
- `logo-bico-quadrada.png`: símbolo branco em fundo laranja, para ícone e uso compacto.

Não redesenhar, recolorir ou gerar variantes da marca. As imagens existentes em `static/branding/favicon/` foram preservadas e ligadas ao template base. Logos oficiais estão integradas à Home mínima; banners oficiais ainda estão pendentes e sua pasta reservada contém apenas instruções.

## Paleta

Valores iniciais alinhados às referências recebidas; as imagens do Figma não foram fornecidas como arquivo de design para inspeção de amostras exatas.

| Token | Valor | Uso |
|---|---|---|
| `--color-primary` | `#FF5308` | Header, ações e destaques laranja |
| `--color-primary-hover` | `#E9470E` | Hover/pressed e texto laranja com contraste |
| `--color-primary-soft` | `#FFF2EB` | Superfície suave de marca |
| `--color-text-primary` | `#253D4E` | Títulos e texto de alta ênfase |
| `--color-text-body` | `#202124` | Texto corrido |
| `--color-text-secondary` | `#66717A` | Texto auxiliar |
| `--color-background` | `#FFFFFF` | Fundo da página |
| `--color-surface` | `#F5F6F7` | Superfície neutra |
| `--color-border` | `#E2E5E8` | Divisórias e contornos |

Não usar paletas roxas/azuis concorrentes nem gradientes decorativos. Laranja, branco e grafite/azul-acinzentado escuro mantêm a linguagem visual das referências.

## Tipografia e uso

As fontes oficiais estão hospedadas localmente em `bico_django/static/fonts/`, com licenças OFL incluídas; a interface não depende de CDN. Tokens de família e peso ficam em `static/css/tokens.css`.

- **Quicksand Bold 700:** títulos principais e de seção, normalmente 24 px / 28,8 px, cor `#253D4E`.
- **Inter Regular 400:** navegação, descrições e textos comuns; menu em 13 px / 24 px.
- **Inter Bold 700:** nomes de profissionais e títulos menores, referência 14 px / 23,8 px.
- **Inter Medium/Semibold 500–600:** botões, preços, filtros e informações de destaque.

Os fallbacks usam famílias sans-serif do sistema; Arial e Roboto não são substitutos visuais principais. Inter variável cobre os pesos da interface; Quicksand é fornecida em 700.

Priorizar contraste, foco de teclado visível, alvos de toque confortáveis e fotografias autorizadas. Fallbacks visuais locais em CSS substituem imagens indisponíveis. Conteúdo de demonstração tem marca explícita; não exibir avaliações, distâncias ou selos de verificação fictícios.
