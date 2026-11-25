# Guia para entender e defender o ETL

Este roteiro explica a implementação em linguagem de apresentação. Leia o código e pratique explicá-lo com suas palavras; a defesa avalia domínio, não leitura do roteiro.

## O que o programa faz, em uma frase

O pipeline busca todas as páginas de clientes e pedidos na API local, guarda uma cópia bruta, normaliza os dados e os carrega em tabelas relacionais. No final, compara a soma dos valores dos itens antes e depois da carga.

## Caminho dos dados

1. **Extração — `etl/extracao.py`:** `consumir_rota` pede página 1, lê `total_pages` e continua até a última. Cada resposta precisa ser HTTP 200 e JSON válido. Um erro de rede, HTTP ou JSON vira mensagem clara. `salvar_bruto` grava a resposta antes da transformação para reprocessar sem depender da API.
2. **Leitura do catálogo — `etl/main.py`:** `csv.DictReader` lê o cabeçalho do CSV e converte `produto_id` para inteiro e preço para número.
3. **Transformação — `etl/transformacao.py`:** funções pequenas recebem um registro e aplicam uma regra. Isso facilita testar cada armadilha sem API nem banco.
4. **Carga — `etl/carga.py`:** primeiro produtos, depois clientes, depois pedidos e seus itens. Assim, cada chave estrangeira já aponta para uma linha existente. SQL parametrizado mantém valores separados do comando SQL.
5. **Reconciliação — `etl/main.py`:** compara as contagens esperadas das quatro tabelas com o banco e compara a soma de `valor_itens` da origem com a soma no destino. Contagem diferente ou diferença monetária acima de um centavo faz o programa terminar com erro.

## As seis armadilhas e como explicar

- **A1 — e-mail ausente:** `None` é gravado como `NULL`, nunca como texto `"None"`. Um sistema não deve inventar informação que não veio da origem.
- **A2 — estado com caixa mista:** `upper()` padroniza as siglas, por exemplo `rs` vira `RS`; a regra mantém o formato esperado pelo banco.
- **A3 — duas datas:** o parser tenta ISO primeiro e dia/mês/ano depois. A saída fica ISO (`AAAA-MM-DD`), formato não ambíguo para o banco.
- **A4 — número ou vírgula decimal:** a string `"125,84"` é convertida para decimal `125.84`. O tipo Decimal evita erro de ponto flutuante em centavos.
- **A5 — pedido repetido entre páginas:** um conjunto de IDs detecta repetição; a primeira ocorrência é mantida. Isso também torna segura a soma e a contagem de pedidos.
- **A6 — total diferente dos itens:** o pipeline preserva `valor_total`, calcula `valor_itens` independentemente e marca `divergente`. Não altera silenciosamente nenhum dos dois valores.

## Por que há duas opções de banco?

PostgreSQL é o destino principal e usa o esquema original. SQLite é a contingência documentada no pacote de insumos; permite demonstrar localmente relacionamentos, transação, carga e reconciliação sem instalar um servidor. A dependência PostgreSQL do projeto é `psycopg[binary]`, e o DSN deve vir de `VERDEJAR_DSN` ou do argumento `--dsn`; o código não deve conter uma senha padrão.

## Por que apagar e recarregar?

Para este conjunto de dados pequeno e completo, substituir as quatro tabelas dentro de uma transação é simples e determinístico. As exclusões respeitam dependências (itens, pedidos, clientes, produtos) e as inserções seguem a ordem inversa. Se alguma inserção falhar, o banco volta ao estado anterior. Em um sistema com grande volume ou histórico, seria melhor fazer upsert incremental e controlar checkpoints.

## Como explicar os testes

`tests/test_transformacao.py` tem casos de entrada e saída esperada para A1 a A6 e verifica que os registros de entrada não são alterados. `tests/test_extracao.py` simula duas páginas HTTP para provar que o laço percorre todas as páginas. `tests/test_reconciliacao.py` carrega duas vezes o mesmo conjunto e compara as contagens das tabelas com as quantidades de origem, além de conferir a soma de `valor_itens`.

## Roteiro da gravação (5–8 minutos)

O briefing exige esta ordem. Faça uma gravação de ensaio antes da versão final e mantenha sua explicação em suas próprias palavras.

1. **Execução do ETL (1–2 min):** mostre a API ativa em um terminal e execute o ETL no segundo terminal. Para demonstrar o destino PostgreSQL previsto no desafio, use `python -m etl.main --banco postgres` com o contêiner ativo. Se optar por SQLite para reduzir o uso do computador, use `python -m etl.main --banco sqlite --sqlite outputs\demonstracao_video.db` e diga claramente que essa gravação usa SQLite; não apresente SQLite como PostgreSQL. Explique os contadores A1–A6 e a reconciliação final. Não mostre senhas ou DSN com credenciais.
2. **Trecho aceito da IA (1–1,5 min):** escolha um trecho que você realmente entende. Explique cada linha, a entrada, a saída e como você verificou o comportamento.
3. **Sugestão rejeitada (1 min):** apresente uma sugestão real da IA, explique por que não se encaixava no contrato e mostre a alternativa implementada.
4. **Testes (1–1,5 min):** execute `python -m pytest -q`, mostre a saída e explique um teste que falhou durante o desenvolvimento e como essa falha foi corrigida. Use uma falha que realmente aconteceu; se não encontrar o registro, não invente uma e peça orientação à coordenação.
5. **Consultas (1 min):** abra `consultas_validacao.sql`, execute a primeira consulta no banco da demonstração e deixe o resultado visível. Para o banco SQLite, no terminal do VS Code, use `python -c "import sqlite3; c=sqlite3.connect('outputs/demonstracao_video.db'); q=open('consultas_validacao.sql', encoding='utf-8').read().split(';')[0]; print(c.execute(q).fetchall())"`. Mostre que a soma dos dez meses é R$ 312.047,75, igual à soma de `valor_total`. Explique também a consulta de pedidos divergentes, que retorna 238 registros.
6. **Fechamento (30 s):** resuma a decisão técnica que considera mais importante e o que você aprendeu.

Antes de gravar, abra a versão corrigida de `Verdejar_Resumo_ETL.xlsx`. No painel, confirme **238 pedidos divergentes** e **4.762 sem divergência**; a tabela mensal também precisa mostrar divergências distribuídas pelos meses. Se usar PostgreSQL, configure `VERDEJAR_DSN` conforme o README. Se usar SQLite, explique a escolha e confirme com a coordenação que a demonstração local atende ao requisito do desafio.

## Perguntas que podem surgir

**Por que preservar os brutos?** Para auditoria e reprocessamento se uma regra de transformação mudar.

**O que acontece se a API cair no meio?** A extração gera uma mensagem com rota e página e para; não carrega silenciosamente um lote parcial como completo.

**Por que comparar soma dos itens, e não `valor_total`?** O campo `valor_itens` é recalculado dos detalhes. A reconciliação prova que o valor calculado no processo foi gravado sem perda. Divergências com o total informado são uma métrica separada.

**O que é idempotência aqui?** Executar o mesmo lote novamente deixa o destino com o mesmo conjunto de linhas, sem crescimento por duplicação.

**O que mudaria com mais uma semana?** Uma boa resposta pessoal deve citar a prioridade que você escolheria (por exemplo, carga incremental, logs estruturados ou validações mais rígidas) e explicar o ganho esperado.

## Itens ainda pessoais

O arquivo de vídeo já foi gravado, mas a versão atual precisa ser substituída antes da publicação: dura 8min23s, termina com um painel antigo que mostra zero divergências e não deixa visível o resultado da consulta mensal. Aumente o zoom do VS Code antes da nova gravação e mantenha a versão final entre 5 e 8 minutos. A reflexão e o texto “Como usei IA” foram aprovados pelo Fellow e confirmados com a coordenação. O Pull Request #1 já foi integrado; `ENTREGA.md` acompanha o que falta para concluir o envio.
