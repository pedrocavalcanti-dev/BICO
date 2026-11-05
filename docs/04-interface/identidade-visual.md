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
| `--color-text-primary` | `#233947` | Títulos e texto de alta ênfase |
| `--color-text-body` | `#202124` | Texto corrido |
| `--color-text-secondary` | `#66717A` | Texto auxiliar |
| `--color-background` | `#FFFFFF` | Fundo da página |
| `--color-surface` | `#F5F6F7` | Superfície neutra |
| `--color-border` | `#E2E5E8` | Divisórias e contornos |

Não usar paletas roxas/azuis concorrentes nem gradientes decorativos. Laranja, branco e grafite/azul-acinzentado escuro mantêm a linguagem visual das referências.

## Tipografia e uso

Usar `Inter` quando já estiver disponível no sistema, com `system-ui`, `Segoe UI` e fontes sans-serif como fallback. A renderização básica não depende de CDN nem de fonte baixada. A escala é curta, fluida para títulos, e mantém espaçamento/altura de linha legíveis.

Priorizar contraste, foco de teclado visível, alvos de toque confortáveis e fotografias reais. Não exibir preços, avaliações, selos ou disponibilidade fictícios.
