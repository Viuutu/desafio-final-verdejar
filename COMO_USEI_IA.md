# Como usei IA

Este arquivo registra a colaboração com IA durante a implementação. Revise e complete com suas palavras antes de entregar. A reflexão e a avaliação do próprio domínio devem ser pessoais.

## Sugestões aceitas

| Sugestão da IA | Onde entrou | Por que aceitei | Como validei |
|---|---|---|---|
| Separar cada armadilha de dados em função pequena e testável. | `etl/transformacao.py`, testes A1–A6 em `tests/test_transformacao.py`. | Regras isoladas ficam mais fáceis de entender, depurar e explicar. | Os testes passam com casos conhecidos de entrada e saída. |
| Preservar as respostas brutas para permitir reprocessamento sem consultar a API novamente. | `etl/extracao.py` grava em `brutos/`; `--reprocessar` usa esses arquivos. | Se uma regra de transformação mudar, não é necessário pedir os dados de novo à API. | Executei o pipeline sobre os JSON fornecidos e rodei a carga duas vezes; as contagens ficaram iguais. |

## Sugestões rejeitadas

As duas sugestões abaixo foram propostas pela IA nesta conversa e rejeitadas por não atenderem ao contrato do desafio.

1. **Sugestão/trecho:** “Use `float` para calcular os valores monetários; é mais simples.” Referia-se a `etl/transformacao.py`, na conversão e soma de valores. **Por que rejeitei:** valores monetários devem preservar os centavos; `float` usa representação binária e pode introduzir diferenças de arredondamento. **Como validei:** os testes A4 verificam a conversão para `Decimal`, e a reconciliação no PostgreSQL terminou com diferença de `0.00`.
2. **Sugestão/trecho:** “Substitua `valor_total` pela soma dos itens para os totais baterem.” Referia-se à regra A6 em `etl/transformacao.py`. **Por que rejeitei:** isso apagaria o valor informado pela origem e esconderia justamente os pedidos que o desafio pede para marcar como divergentes. **Como validei:** mantive `valor_total` e `valor_itens` em colunas separadas; a carga identificou 238 pedidos divergentes e a consulta em `consultas_validacao.sql` permite inspecioná-los.

## Falhas e retrabalho

Na primeira execução com `python -m etl.main`, a IA importava os módulos internos como se o arquivo sempre fosse iniciado diretamente; a execução como módulo falhou com `ModuleNotFoundError: No module named 'extracao'`. O retrabalho foi permitir importações relativas quando executado como módulo e importações locais quando iniciado diretamente. Validei com `python -m etl.main --banco sqlite --reprocessar`.

## Reflexão pessoal para a entrega (10–20 linhas)

Rascunho baseado no que aconteceu nesta conversa; revise para confirmar que representa sua experiência e ajuste as palavras antes de entregar:

Minha maior dificuldade foi colocar as partes para funcionarem juntas: API, terminal do VS Code e PostgreSQL no Docker.
No começo, misturei comandos e não sabia se a API estava iniciada.
Aprendi que a API precisa ficar rodando em um terminal próprio.
Usei outro terminal para testar a rota de saúde e executar o ETL.
Também não lembrava a senha do banco, então precisei recuperar a configuração do contêiner.
A IA me ajudou a estruturar a extração, as transformações, a carga e os testes.
Eu fiz questão de acompanhar os comandos e entender o que cada etapa estava fazendo.
Verifiquei que a API respondia antes de continuar.
Depois observei a saída do ETL e confirmei que os pedidos foram carregados.
Rodei o processo novamente para conferir que a segunda execução não duplicava pedidos.
Entendi que a reconciliação compara a soma dos itens calculada com a soma gravada no banco.
Também aprendi que não devo substituir o total informado pela origem só para esconder uma divergência.
Se tivesse mais uma semana, eu simplificaria a inicialização para deixar API e banco mais fáceis de subir e validar.
Também praticaria a explicação das funções de transformação antes de gravar a defesa oral.
