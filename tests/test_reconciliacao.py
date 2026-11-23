import sqlite3
from decimal import Decimal

from etl.carga import carregar_sqlite
from etl.transformacao import transformar


def test_carga_sqlite_idempotente_e_reconciliada(tmp_path):
    dados, _ = transformar(
        [{"id": 1, "nome": "A", "email": None, "cidade": "X", "estado": "rs", "cadastro_em": "2026-01-01"}],
        [{"id": 1, "cliente_id": 1, "data_pedido": "01/01/2026", "status": "entregue",
          "valor_total": "10,00", "itens": [{"produto_id": 1, "quantidade": 2, "preco_unitario": 5.0}]}],
        [{"produto_id": 1, "nome": "P", "categoria": "frutas", "preco_base": 5.0}])
    dbfile = str(tmp_path / "test.db")
    schema = "insumos/schema_sqlite.sql"
    expected_counts = {
        "clientes": len(dados["clientes"]),
        "produtos": len(dados["produtos"]),
        "pedidos": len(dados["pedidos"]),
        "itens_pedido": sum(len(p["itens"]) for p in dados["pedidos"]),
    }
    expected_total = sum((p["valor_itens"] for p in dados["pedidos"]), Decimal("0.00"))
    executions = []
    for _ in range(2):
        db = carregar_sqlite(dbfile, dados, schema)
        try:
            counts = {table: db.execute("SELECT COUNT(*) FROM " + table).fetchone()[0]
                      for table in expected_counts}
            total = db.execute("SELECT SUM(valor_itens) FROM pedidos").fetchone()[0]
            executions.append((counts, Decimal(str(total))))
        finally:
            db.close()

    assert executions[0] == executions[1]
    assert executions[0][0] == expected_counts
    assert abs(executions[0][1] - expected_total) <= Decimal("0.01")
