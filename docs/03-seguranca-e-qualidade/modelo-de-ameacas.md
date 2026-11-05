# Modelo de ameaças inicial

| Ativo | Ameaça | Direção de controle |
|---|---|---|
| Contas | enumeração, credencial fraca, abuso de login | mensagens neutras, validação, throttling e recuperação segura no Alpha 0.2 |
| Solicitações | IDOR, transição indevida, falso aceite/conclusão | checagem de participante e máquina de estados no servidor |
| Conversas | leitura por terceiros, exposição em logs | autorização por participante, minimização e retenção limitada |
| Localização | exposição de endereço residencial | divulgar região aproximada e restringir coordenadas privadas |
| Configuração | secret ou senha no Git | `.env` ignorado, produção fail-closed e revisão antes de commit |
| Operação | abuso administrativo sem rastreio | permissões mínimas e auditoria de eventos pertinentes |

Este é um ponto de partida e não substitui análise de risco de cada funcionalidade.
