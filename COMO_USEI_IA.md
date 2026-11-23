# Como usei IA

## Meu projeto e minha colaboração

Desenvolvi, com apoio de IA, um ETL para a loja fictícia Verdejar. O processo extrai clientes e pedidos de uma API paginada, lê o catálogo de produtos em CSV, trata seis problemas de qualidade, carrega os dados no PostgreSQL e confere se a carga preservou os totais. Também preparei testes, consultas SQL, documentação e uma planilha editável com indicadores e gráficos.

Usei a IA como apoio em partes substanciais do código e da documentação, e não apenas para sugerir uma função isolada. Esse escopo foi mais amplo do que o papel limitado recomendado no desafio. Quero ser transparente sobre isso. Minha iniciativa foi definir o que precisava ser feito, configurar e usar Docker e VS Code, executar os comandos, mostrar os erros que apareciam e pedir explicações até entender melhor cada etapa. Não me contentei em receber arquivos: fiz perguntas, acompanhei a API e conferi os resultados do processo. Tenho orgulho da minha persistência e da disposição de aprender mesmo quando os primeiros comandos falharam.

## Sugestões aceitas

1. **Sugestão:** separar cada armadilha de qualidade em uma função pequena e testável. **Onde entrou:** `etl/transformacao.py` e `tests/test_transformacao.py`. **Por que aceitei:** assim consigo explicar e verificar cada regra separadamente. **Como validei:** os testes cobrem A1–A6 e também verificam que as funções não alteram os dados recebidos; a revisão atual tem 11 testes.
2. **Sugestão:** guardar as respostas brutas antes de transformar os dados, para permitir reprocessamento sem consultar a API novamente. **Onde entrou:** `etl/extracao.py` salva JSON em `brutos/`, e `--reprocessar` os lê. **Por que aceitei:** se uma regra mudar, posso reaplicá-la aos mesmos dados. **Como validei:** a carga repetida manteve as mesmas contagens e totais.
3. **Sugestão:** manter a API rodando em um terminal e usar outro terminal do VS Code para testar a rota de saúde e executar o ETL. **Por que aceitei:** isso me ajudou a perceber quando o problema era a API ainda não estar ativa. **Como validei:** consultei `/saude` depois de iniciar o serviço e então acompanhei os pedidos retornados.
4. **Sugestão:** configurar a conexão do banco por variável de ambiente, sem colocar a senha no código ou no README. **Onde entrou:** uso de `VERDEJAR_DSN` documentado no README. **Por que aceitei:** evita expor credenciais e permite configurar cada ambiente. **Como validei:** o projeto foi executado com PostgreSQL no Docker e as cargas mantiveram as mesmas contagens.

## Sugestões rejeitadas

As sugestões abaixo refletem decisões técnicas que consigo relacionar ao histórico e ao código do projeto. Antes da entrega, confirme se você se lembra delas da mesma forma; não apresente como fala literal uma formulação reconstruída agora.

1. **Sugestão:** usar `float` nos cálculos monetários por ser mais simples. **Por que rejeitei:** valores monetários podem sofrer imprecisão de representação binária. **O que fiz no lugar:** mantive `Decimal` na transformação para preservar os centavos. **Como validei:** o teste A4 verifica o valor convertido, e a reconciliação registrada ficou com diferença de R$ 0,00.
2. **Sugestão:** substituir `valor_total` pela soma dos itens para fazer os valores baterem. **Por que rejeitei:** isso apagaria o valor informado pela origem e esconderia as divergências. **O que fiz no lugar:** mantive `valor_total` e `valor_itens` separados e marquei os pedidos divergentes. **Como validei:** o processo encontrou 238 divergências, consultáveis em `consultas_validacao.sql`.
3. **Decisão rejeitada na revisão:** manter uma senha padrão do PostgreSQL no código para facilitar a execução. A versão inicial tinha uma senha de exemplo no DSN. **Por que rejeitei:** credenciais não devem ficar embutidas no programa. **O que fiz no lugar:** removi o valor padrão e passei a exigir `VERDEJAR_DSN` ou `--dsn`. **Como validei:** a suíte passou e a execução PostgreSQL agora exige configuração explícita da conexão.

## Docker, erros e retrabalho

Com orientação, conectei o VS Code ao Docker e subi o PostgreSQL em um contêiner. No começo, tive dificuldade para saber se a API estava ativa e misturei comandos do PowerShell: a primeira chamada de `/saude` ficou concatenada com a ativação do ambiente e produziu erro de parâmetros. Depois, separei as etapas, iniciei a API em um terminal do VS Code e usei outro terminal para verificar a rota e acompanhar os pedidos. Esse processo me ensinou a ler o erro antes de repetir o comando e a conferir cada serviço por vez.

Também houve uma falha nos imports internos: `python -m etl.main` apresentou `ModuleNotFoundError: No module named 'extracao'`. A estrutura dos imports foi ajustada para permitir a execução como módulo e diretamente. Foi um erro de execução, não uma falha do pytest; o fluxo foi conferido com `python -m etl.main --banco sqlite --reprocessar`.

Na planilha, uma primeira versão das fórmulas usou referências de linha deslocadas. A IA corrigiu o mapeamento e conferiu os cálculos. Uma alteração temporária em um pedido fez as divergências mudarem de 238 para 237 e retornarem a 238 quando o valor original foi restaurado. Esse ajuste foi feito pela IA; não vou afirmar que corrigi o código sozinho.

## Reflexão pessoal

Quando comecei este desafio, eu ainda não sabia muito bem como uma API, um programa em Python e um banco de dados trabalhavam juntos.<br>
Ao longo do projeto, fui acompanhando a montagem do ETL e comecei a entender o caminho que os dados percorrem.<br>
Uma das partes que mais me confundiu foi descobrir por que alguns totais dos pedidos não batiam com a soma dos itens.<br>
Depois entendi que corrigir o total recebido só para os números coincidirem esconderia uma informação importante.<br>
Por isso, o projeto mantém o valor informado pela origem, calcula a soma dos itens separadamente e sinaliza as diferenças.<br>
Também tive dificuldade para organizar os terminais do VS Code, iniciar a API e conectar o PostgreSQL no Docker.<br>
Quando um comando falhou, precisei parar, olhar a mensagem e tentar entender o que estava acontecendo em vez de apenas repetir.<br>
Usei a IA em partes importantes do código, dos testes, da documentação e da planilha, e reconheço que essa ajuda foi ampla.<br>
Isso foi além do papel limitado recomendado no desafio, então quero ser transparente sobre como trabalhei.<br>
Minha contribuição foi definir o que eu precisava entregar, configurar as ferramentas, executar os passos e trazer minhas dúvidas e resultados.<br>
Ainda estou aprendendo, mas hoje consigo explicar melhor como a extração, a transformação, a carga e a validação se conectam.<br>
Na revisão atual, os 11 testes passaram; a reconciliação registrada para o banco teve diferença de R$ 0,00.<br>
Se eu tivesse mais uma semana, deixaria a inicialização dos serviços mais simples e praticaria a apresentação do projeto.<br>
Antes da defesa, quero revisar as decisões com calma para conseguir explicá-las com minhas palavras, sem apenas ler o código.
O que mais levo deste desafio é que pedir ajuda também exige conferir o resultado e assumir responsabilidade pelo que vou apresentar.
