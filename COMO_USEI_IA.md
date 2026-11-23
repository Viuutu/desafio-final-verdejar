# Como usei IA

## Meu projeto e minha colaboração

Desenvolvi, com apoio de IA, um ETL para a loja fictícia Verdejar. O processo extrai clientes e pedidos de uma API paginada, lê o catálogo de produtos em CSV, trata seis problemas de qualidade, carrega os dados no PostgreSQL e confere se a carga preservou os totais. Também preparei testes, consultas SQL, documentação e uma planilha editável com indicadores e gráficos.

Usei a IA como apoio em partes substanciais do código e da documentação, e não apenas para sugerir uma função isolada. Esse escopo foi mais amplo do que o papel limitado recomendado no desafio. Quero ser transparente sobre isso. Minha iniciativa foi definir o que precisava ser feito, configurar e usar Docker e VS Code, executar os comandos, mostrar os erros que apareciam e pedir explicações até entender melhor cada etapa. Não me contentei em receber arquivos: fiz perguntas, acompanhei a API e conferi os resultados do processo. Tenho orgulho da minha persistência e da disposição de aprender mesmo quando os primeiros comandos falharam.

## Sugestões aceitas

1. **Sugestão:** separar cada armadilha de qualidade em uma função pequena e testável. **Onde entrou:** `etl/transformacao.py` e `tests/test_transformacao.py`. **Por que aceitei:** assim consigo explicar e verificar cada regra separadamente. **Como validei:** os testes cobrem A1–A6; a execução registrada do pytest terminou com 10 testes aprovados.
2. **Sugestão:** guardar as respostas brutas antes de transformar os dados, para permitir reprocessamento sem consultar a API novamente. **Onde entrou:** `etl/extracao.py` salva JSON em `brutos/`, e `--reprocessar` os lê. **Por que aceitei:** se uma regra mudar, posso reaplicá-la aos mesmos dados. **Como validei:** a carga repetida manteve as mesmas contagens e totais.
3. **Sugestão:** manter a API rodando em um terminal e usar outro terminal do VS Code para testar a rota de saúde e executar o ETL. **Por que aceitei:** isso me ajudou a perceber quando o problema era a API ainda não estar ativa. **Como validei:** consultei `/saude` depois de iniciar o serviço e então acompanhei os pedidos retornados.
4. **Sugestão:** configurar a conexão do banco por variável de ambiente, sem colocar a senha no código ou no README. **Onde entrou:** uso de `VERDEJAR_DSN` documentado no README. **Por que aceitei:** evita expor credenciais e permite configurar cada ambiente. **Como validei:** o projeto foi executado com PostgreSQL no Docker e as cargas mantiveram as mesmas contagens.

## Sugestões rejeitadas

As duas primeiras sugestões já constavam no registro anterior do projeto. Confira se as palavras abaixo correspondem às propostas que realmente apareceram na conversa; se não, substitua-as por sugestões reais antes de entregar.

1. **Sugestão:** usar `float` nos cálculos monetários por ser mais simples. **Por que rejeitei:** valores monetários podem sofrer imprecisão de representação binária. **O que fiz no lugar:** mantive `Decimal` na transformação para preservar os centavos. **Como validei:** o teste A4 verifica o valor convertido, e a reconciliação registrada ficou com diferença de R$ 0,00.
2. **Sugestão:** substituir `valor_total` pela soma dos itens para fazer os valores baterem. **Por que rejeitei:** isso apagaria o valor informado pela origem e esconderia as divergências. **O que fiz no lugar:** mantive `valor_total` e `valor_itens` separados e marquei os pedidos divergentes. **Como validei:** o processo encontrou 238 divergências, consultáveis em `consultas_validacao.sql`.

3. **Sugestão — juntar ativação do ambiente, inicialização da API e chamada HTTP em um único comando do PowerShell.** Eu passei a executar as etapas separadamente depois que o comando combinado deu erro de parâmetros e a chamada à API não conectou. **Como validar a decisão:** ativar o ambiente, iniciar a API em um terminal e chamar `/saude` em outro. Esta foi uma alternativa de execução que abandonei; não a apresente como sugestão da IA se ela veio do meu próprio comando.

## Docker, erros e retrabalho

Com orientação, conectei o VS Code ao Docker e subi o PostgreSQL em um contêiner. No começo, tive dificuldade para saber se a API estava ativa e misturei comandos do PowerShell: a primeira chamada de `/saude` ficou concatenada com a ativação do ambiente e produziu erro de parâmetros. Depois, separei as etapas, iniciei a API em um terminal do VS Code e usei outro terminal para verificar a rota e acompanhar os pedidos. Esse processo me ensinou a ler o erro antes de repetir o comando e a conferir cada serviço por vez.

Também houve uma falha nos imports internos: `python -m etl.main` apresentou `ModuleNotFoundError: No module named 'extracao'`. A implementação foi ajustada para usar imports relativos quando executada como módulo e imports locais quando executada diretamente; o fluxo foi conferido com `python -m etl.main --banco sqlite --reprocessar`.

Na planilha, uma primeira versão das fórmulas usou referências de linha deslocadas. A IA corrigiu o mapeamento e conferiu os cálculos. Uma alteração temporária em um pedido fez as divergências mudarem de 238 para 237 e retornarem a 238 quando o valor original foi restaurado. Esse ajuste foi feito pela IA; não vou afirmar que corrigi o código sozinho.

## Reflexão pessoal (rascunho — 15 linhas)

Minha maior conquista neste desafio foi acompanhar a construção de um ETL completo e entender como a API, o Python e o PostgreSQL se conectam. A decisão técnica mais difícil foi compreender como tratar os pedidos cujo total informado não corresponde à soma dos itens. Aprendi que não devemos alterar o valor recebido apenas para fazer os números coincidirem; o projeto preserva o total original, calcula o valor dos itens separadamente e sinaliza as divergências. No começo, tive dificuldade para organizar a execução da API e do banco no Docker e para usar os terminais do VS Code. Mesmo quando os primeiros comandos falharam, continuei compartilhando os erros e buscando entender cada etapa. Usei a IA de forma ampla para ajudar na implementação do ETL, nos testes, na documentação e na planilha, e reconheço que isso foi além do papel limitado recomendado pelo desafio. Minha participação foi definir os objetivos, configurar e usar as ferramentas, executar comandos no meu ambiente, acompanhar os resultados e pedir explicações para aprender. A validação registrada no projeto mostra 10 testes aprovados e uma reconciliação sem diferença. Se tivesse mais uma semana, simplificaria a inicialização da API e do PostgreSQL e praticaria a explicação do código e dos testes para defender as decisões com mais segurança.