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
    for _ in range(2):
        db = carregar_sqlite(dbfile, dados, schema); db.close()
    db = sqlite3.connect(dbfile)
    assert db.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0] == 1
    assert db.execute("SELECT COUNT(*) FROM itens_pedido").fetchone()[0] == 1
    assert Decimal(str(db.execute("SELECT SUM(valor_itens) FROM pedidos").fetchone()[0])) == Decimal("10.0")
    db.close()
