-- (a) Vendas por mes (receita considerada: soma dos valores informados nos pedidos).
-- substr funciona com a data DATE do PostgreSQL e o texto ISO do SQLite.
SELECT substr(CAST(data_pedido AS TEXT), 1, 7) AS mes,
       ROUND(SUM(valor_total), 2) AS vendas
FROM pedidos
GROUP BY substr(CAST(data_pedido AS TEXT), 1, 7)
ORDER BY mes;

-- (b) Quantidade de pedidos por estado do cliente.
SELECT c.estado, COUNT(*) AS quantidade_pedidos
FROM pedidos p JOIN clientes c ON c.id = p.cliente_id
GROUP BY c.estado
ORDER BY c.estado;

-- (c) Pedidos com total informado divergente da soma dos itens.
SELECT id AS pedido_id, valor_total, valor_itens,
       ROUND(valor_total - valor_itens, 2) AS diferenca
FROM pedidos
WHERE divergente = 1
ORDER BY id;
