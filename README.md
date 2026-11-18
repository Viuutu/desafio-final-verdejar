# Projeto final — ETL da Verdejar

Implementação do desafio final do Bootcamp: extração de clientes e pedidos da API local, leitura do catálogo de produtos, transformação dos dados e carga em PostgreSQL.

## Estado inicial

A estrutura local do projeto está preparada. Os arquivos de insumo originais ainda precisam ser copiados para `insumos/`: `gerar_dados.py`, `api_verdejar.py`, `dados/produtos.csv`, `schema.sql` e `README_insumos.md`. A implementação depende desses arquivos para seguir o contrato real da API e do banco.

## Ambiente

- Python 3.8.2 disponível nesta máquina.
- Git 2.45.2 disponível.
- Docker ainda não está disponível como comando no terminal; é necessário confirmar/instalar e iniciar o Docker Desktop para executar o PostgreSQL.

## Estrutura

```text
insumos/    arquivos fornecidos pelo curso
etl/        código do pipeline
brutos/     respostas extraídas para reprocessamento (não versionadas)
tests/      testes automatizados
```

## Próximos passos

1. Copiar os insumos originais para `insumos/`.
2. Iniciar a API e validar `/saude`.
3. Subir o PostgreSQL com Docker e aplicar `schema.sql`.
4. Implementar extração, transformação, carga e testes conforme o briefing.
