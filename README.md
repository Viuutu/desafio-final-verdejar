# Projeto final — ETL da Verdejar

Pipeline em Python que lê clientes e pedidos da API local paginada, preserva os dados brutos, transforma os seis casos de qualidade descritos no desafio e carrega produtos, clientes, pedidos e itens em um banco relacional. O banco padrão local é SQLite; a execução principal do desafio pode ser feita com PostgreSQL usando `--banco postgres`.

## Entregáveis incluídos

- `insumos/`: cópia dos dados, API e esquemas recebidos.
- `etl/`: extração, transformação, carga e orquestração.
- `brutos/`: respostas da API para reprocessamento (gerado localmente, ignorado pelo Git).
- `tests/`: nove testes com pytest.
- `CONTRATO_DE_DADOS.md`: campos, tipos, nulabilidade e regras.
- `consultas_validacao.sql`: as três consultas pedidas.
- `GUIA_DE_DEFESA.md`: explicação didática e roteiro para apresentação.
- `COMO_USEI_IA.md`: registro do uso de IA e pontos de reflexão.
- `ENTREGA.md`: checklist para o upload, PR e gravação.
- `Verdejar_Resumo_ETL.xlsx`: planilha editável com painel, tabelas e gráficos de vendas e qualidade dos pedidos.

### Abrir a planilha

[Abrir ou baixar o painel de vendas no Excel](./Verdejar_Resumo_ETL.xlsx). No GitHub, o link abre a visualização do arquivo; você também pode baixá-lo para editar no Excel.

## Requisitos

- Python 3.8 ou superior.
- Para validar o projeto: `python -m pip install -r requirements.txt` (inclui pytest; psycopg2 só é usado com PostgreSQL).
- Para PostgreSQL: Docker Desktop ou PostgreSQL instalado, mais `psycopg[binary]` (incluído em `requirements.txt`).
- Alternativa sem instalar banco: SQLite, já incluído no Python.

## Rodar no SQLite (caminho rápido)

Abra dois terminais na pasta raiz.

Terminal 1 — API:

```powershell
python insumos/api_verdejar.py --porta 8000 --dados insumos/dados
```

Terminal 2 — ETL:

```powershell
python -m etl.main --banco sqlite
```

O programa cria `verdejar.db`, salva os JSON recebidos em `brutos/` e imprime páginas, registros, contadores, linhas carregadas e reconciliação. A saída deverá terminar com diferença de `0.00`.

Para reprocessar sem API:

```powershell
python -m etl.main --banco sqlite --reprocessar
```

## Rodar no PostgreSQL (destino principal)

Suba PostgreSQL local pelo método escolhido no desafio. Para Docker:

```powershell
docker run --name verdejar-pg -e POSTGRES_PASSWORD=troque_esta_senha -e POSTGRES_DB=verdejar -p 5432:5432 -d postgres:16
```

Instale as dependências e configure uma variável de ambiente com os dados de conexão (não coloque senha no código, Git ou README):

```powershell
python -m pip install -r requirements.txt
$env:VERDEJAR_DSN = "dbname=verdejar user=postgres password=SUA_SENHA host=localhost port=5432"
```

Aplique o esquema dentro do contêiner e rode:

```powershell
Get-Content insumos/schema.sql | docker exec -i verdejar-pg psql -U postgres -d verdejar
python -m etl.main --banco postgres
```

O destino SQLite usa `insumos/schema_sqlite.sql`; PostgreSQL usa o esquema oficial `insumos/schema.sql`.

O VS Code deste computador está com a extensão oficial **Container Tools** instalada (`ms-azuretools.vscode-containers`). Ela usa o Docker Desktop e o contexto Docker padrão. Para validar a carga, iniciei um contêiner temporário, executei o ETL duas vezes e removi o contêiner ao terminar.

## Testes

```powershell
python -m pytest -q
```

Os testes cobrem as armadilhas A1–A6, a paginação e a carga/reconciliação idempotente. O teste de extração simula respostas de duas páginas, sem depender de uma porta de rede local.

## Resultados calculados com os dados da seed 2026

Execução sobre os JSON fornecidos. A carga foi executada duas vezes em SQLite e duas vezes no PostgreSQL do Docker; as contagens e os totais permaneceram iguais nos dois destinos.

| Métrica | Resultado |
|---|---:|
| Clientes recebidos | 1.000 |
| Pedidos recebidos da origem (com repetições) | 5.100 |
| Pedidos únicos | 5.000 |
| Repetições descartadas | 100 |
| Produtos | 12 |
| Itens de pedido | 12.455 |
| E-mails nulos preservados | 81 |
| Estados corrigidos para maiúsculas | 151 |
| Datas no formato dia/mês/ano convertidas | 1.037 |
| Valores em texto convertidos | 1.255 |
| Pedidos divergentes (tolerância de um centavo) | 238 |
| Soma de `valor_itens` na origem transformada | R$ 311.228,75 |
| Soma de `valor_itens` no banco | R$ 311.228,75 |
| Diferença de reconciliação | R$ 0,00 |
| Testes aprovados | 10 |

Vendas por mês (soma de `valor_total`): janeiro R$ 30.449,02; fevereiro R$ 33.923,86; março R$ 30.678,70; abril R$ 31.253,96; maio R$ 30.890,02; junho R$ 31.627,73; julho R$ 32.796,17; agosto R$ 29.328,04; setembro R$ 29.995,71; outubro R$ 31.104,54. A soma dos meses é R$ 312.047,75. Ela difere da soma de `valor_itens` porque 238 pedidos têm divergências entre o total informado e os itens.

Pedidos por estado do cliente: MG 476; PR 974; RS 1.543; SC 1.127; SP 880.

## Decisões e limites

A carga apaga e recria o conjunto completo em uma transação para oferecer resultado repetível em um dataset didático. Dados brutos são guardados antes de transformar. O campo original `valor_total` é preservado; `valor_itens` é calculado separadamente e divergências são sinalizadas, sem correção silenciosa.

A chamada HTTP local à API não foi possível de validar a partir deste ambiente de execução: a conexão a `127.0.0.1:8000` expirou. A função paginada foi validada por teste simulado, e o pipeline inteiro foi executado com os mesmos JSON que acompanham os insumos. Faça a demonstração com a API ativa no VS Code/terminal local.

## Próximos passos do Fellow

Antes do upload, leia `ENTREGA.md`, preencha a reflexão pessoal (10–20 linhas), revise o registro de IA com suas interações reais, publique o Pull Request, grave e publique o vídeo de 5–8 minutos. O roteiro técnico está em `GUIA_DE_DEFESA.md`; personalize-o para falar com suas palavras.
