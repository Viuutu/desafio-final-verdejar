# Contrato de dados do ETL Verdejar

O contrato descreve o formato esperado na origem e o formato persistido no banco. Os dados de entrada são sintéticos e ficam em `insumos/dados/`.

## clientes → clientes

| Campo | Tipo no destino | Nulo? | Regra |
|---|---|---:|---|
| `id` | INTEGER / PK | Não | Identificador da API; chave primária. |
| `nome` | TEXT | Não | Preservado da origem. |
| `email` | TEXT | Sim | E-mail ausente continua `NULL` (A1); espaços externos são removidos. |
| `cidade` | TEXT | Não | Preservada da origem. |
| `estado` | CHAR(2) / TEXT | Não | Sigla em duas letras maiúsculas (A2). |
| `cadastro_em` | DATE / texto ISO | Não | Data ISO recebida do arquivo de clientes. |

## produtos.csv → produtos

| Campo | Tipo no destino | Nulo? | Regra |
|---|---|---:|---|
| `produto_id` | INTEGER / PK | Não | Convertido de texto CSV para inteiro. |
| `nome` | TEXT | Não | Preservado. |
| `categoria` | TEXT | Não | Preservada. |
| `preco_base` | NUMERIC(10,2) | Não | Convertido para valor numérico. |

## pedidos da API → pedidos e itens_pedido

| Campo | Destino | Nulo? | Regra |
|---|---|---:|---|
| `id` | `pedidos.id`, INTEGER / PK | Não | A5: manter a primeira ocorrência por ID. |
| `cliente_id` | `pedidos.cliente_id`, FK | Não | Deve apontar para `clientes.id`. |
| `data_pedido` | DATE / texto ISO | Não | Aceitar `AAAA-MM-DD` e `DD/MM/AAAA`; armazenar ISO (A3). |
| `status` | TEXT | Não | Preservado da API. |
| `valor_total` | NUMERIC(12,2) | Não | Número ou texto com vírgula decimal convertido para duas casas (A4). |
| soma dos itens | `pedidos.valor_itens`, NUMERIC(12,2) | Não | Soma de `quantidade × preco_unitario`, arredondada a centavos. |
| divergência | `pedidos.divergente`, BOOLEAN / INTEGER | Não | Verdadeiro se `abs(valor_total - valor_itens) > 0,01` (A6). |

Cada elemento `itens[]` vira uma linha em `itens_pedido`. `linha` é a posição (começa em 1), e o par `(pedido_id, linha)` forma a chave primária. `produto_id` referencia `produtos.produto_id`.

## Idempotência e estratégia de carga

Cada execução substitui as tabelas de destino em uma única transação, respeitando a ordem das chaves estrangeiras. Se a carga falhar, a transação é revertida. Reexecutar a mesma entrada produz uma cópia consistente, sem duplicar linhas. A extração bruta fica em `brutos/` para permitir reprocessamento sem nova chamada à API.
