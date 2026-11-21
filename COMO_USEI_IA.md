# Como usei IA

## Estado deste registro

Este arquivo ainda é um rascunho e não está pronto para o upload. O Fellow informou que ainda vai escrever a reflexão e gravar o vídeo. Os exemplos de sugestões aceitas e rejeitadas precisam ser conferidos com as interações reais antes de serem apresentados como decisões pessoais.

## Escopo real de colaboração observado

A IA participou de partes substanciais do projeto: implementação e ajustes do ETL, documentação, testes, planilha Excel, comandos Git e preparação do pull request. Isso foi mais amplo do que o papel limitado recomendado no briefing (a IA propõe funções e testes dentro de um escopo definido pelo Fellow). Esse fato deve ser explicado com honestidade na entrega e na defesa, sem dizer que a IA apenas sugeriu pequenos trechos.

O Fellow definiu o objetivo, configurou e usou Docker/VS Code, executou comandos no terminal, compartilhou erros e resultados, acompanhou a API e pediu explicações para entender o projeto. Antes de entregar, confirme que essa descrição representa sua participação e acrescente o que você fez diretamente no código.

## Sugestões aceitas — completar com exemplos reais

O briefing pede pelo menos duas sugestões aceitas, com o trecho sugerido, onde foi aplicado, motivo da decisão e validação. Não atribua uma sugestão à IA sem confirmar que ela ocorreu.

1. **Trecho exato ou fiel da sugestão:** `[completar]` — **Onde entrou:** `[arquivo e função]` — **Por que aceitei:** `[completar com sua decisão]` — **Como validei:** `[comando, teste ou resultado observado]`

2. **Trecho exato ou fiel da sugestão:** `[completar]` — **Onde entrou:** `[arquivo e função]` — **Por que aceitei:** `[completar com sua decisão]` — **Como validei:** `[comando, teste ou resultado observado]`

## Sugestões rejeitadas — completar com exemplos reais

O briefing pede pelo menos duas sugestões rejeitadas, com o trecho sugerido, motivo da rejeição e validação da alternativa. Use somente sugestões que a IA realmente apresentou nesta interação.

1. **Trecho exato ou fiel da sugestão:** `[completar]` — **Por que rejeitei:** `[completar]` — **O que fiz no lugar:** `[completar]` — **Como validei:** `[comando, teste ou resultado observado]`

2. **Trecho exato ou fiel da sugestão:** `[completar]` — **Por que rejeitei:** `[completar]` — **O que fiz no lugar:** `[completar]` — **Como validei:** `[comando, teste ou resultado observado]`

## Falha e retrabalho observados

No desenvolvimento do ETL, a primeira versão dos imports internos falhou ao executar `python -m etl.main`, com `ModuleNotFoundError: No module named 'extracao'`. A versão foi ajustada para usar imports relativos quando o código roda como módulo e imports locais quando executado diretamente; o fluxo foi então validado com `python -m etl.main --banco sqlite --reprocessar`. Confirme essa sequência com sua experiência antes de apresentá-la.

Durante a montagem da planilha, a primeira versão de algumas fórmulas usou referências de linha deslocadas. Isso causou erros de cálculo. A IA corrigiu a conversão entre o índice dos registros e a linha do Excel (os dados começam na linha 2), recalculou as fórmulas e verificou que não restaram erros. Também alterou temporariamente o valor informado de um pedido: o painel passou de 238 para 237 divergências e voltou a 238 quando o valor foi restaurado.

Esse retrabalho foi feito pela IA nesta sessão. Não o descreva como uma correção feita pelo Fellow. Se o briefing exigir que você explique uma falha corrigida por você, escolha uma falha que você tenha realmente reproduzido e corrigido, ou combine com a coordenação como apresentar este caso de forma fiel.

## Reflexão pessoal (10–20 linhas) — pendente

O Fellow informou que ainda não escreveu a reflexão. Escreva-a com suas palavras para responder:

- Qual foi a decisão mais difícil do ETL e por quê?
- O que você delegou à IA e o que fez questão de fazer sozinho?
- Se tivesse mais uma semana, o que mudaria primeiro?

Não envie esta seção enquanto ela estiver sem a reflexão final.
