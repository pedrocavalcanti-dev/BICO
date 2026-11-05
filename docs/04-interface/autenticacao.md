# Interface de autenticação

Login, cadastro e recuperação de senha compartilham o layout claro/laranja BICO, o aside institucional e os tokens de marca. Quicksand é usada nos títulos e Inter na interface. O formulário vem primeiro em telas estreitas; o conteúdo institucional é simplificado em mobile. CSS e JavaScript são locais.

Campos têm labels associados, erros próximos ao controle, foco visível e mensagens anunciadas por leitores de tela. O botão de senha alterna visibilidade com estado acessível. Submissões mostram estado ocupado sem depender de alertas. Não há botões sociais aparentando integração.

As páginas compartilham `base.html`; os blocos de cabeçalho/rodapé podem ser ocultados no fluxo de autenticação sem duplicar o layout global. A validação em viewports é registrada em `docs/01-projeto/estado-atual.md` após a revisão visual.
