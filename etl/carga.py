# -*- coding: utf-8 -*-
"""Carga transacional e idempotente para PostgreSQL ou SQLite."""
import sqlite3
from decimal import Decimal


def _valor(valor):
    return float(valor) if isinstance(valor, Decimal) else valor


def carregar_sqlite(caminho, dados, schema):
    conexao = sqlite3.connect(caminho)
    try:
        conexao.execute("PRAGMA foreign_keys = ON")
        conexao.executescript(open(schema, encoding="utf-8").read())
        with conexao:
            # Recriar o conjunto de origem torna a carga reexecutavel e sem duplicacao.
            for tabela in ("itens_pedido", "pedidos", "clientes", "produtos"):
                conexao.execute("DELETE FROM " + tabela)
            conexao.executemany("INSERT INTO produtos VALUES (?, ?, ?, ?)", [
                (p["produto_id"], p["nome"], p["categoria"], p["preco_base"]) for p in dados["produtos"]])
            conexao.executemany("INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?)", [
                (c["id"], c["nome"], c["email"], c["cidade"], c["estado"], c["cadastro_em"])
                for c in dados["clientes"]])
            for p in dados["pedidos"]:
                conexao.execute("INSERT INTO pedidos VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (p["id"], p["cliente_id"], p["data_pedido"], p["status"], _valor(p["valor_total"]),
                     _valor(p["valor_itens"]), int(p["divergente"])))
                conexao.executemany("INSERT INTO itens_pedido VALUES (?, ?, ?, ?, ?)", [
                    (p["id"], i, item["produto_id"], item["quantidade"], item["preco_unitario"])
                    for i, item in enumerate(p["itens"], 1)])
        return conexao
    except Exception:
        conexao.close()
        raise


def carregar_postgres(dsn, dados):
    try:
        import psycopg
        psycopg3 = True
    except ImportError:
        try:
            import psycopg2
        except ImportError:
            raise RuntimeError("Instale psycopg[binary] ou psycopg2-binary para usar PostgreSQL.")
        conectar = psycopg2.connect
        psycopg3 = False
    else:
        conectar = psycopg.connect
    conexao = conectar(dsn)
    try:
        # psycopg 3 fecha a conexao ao sair de `with conexao`; transaction()
        # delimita a transacao sem fecha-la, para permitir a reconciliacao posterior.
        transacao = conexao.transaction() if psycopg3 else conexao
        with transacao:
            with conexao.cursor() as cur:
                for tabela in ("itens_pedido", "pedidos", "clientes", "produtos"):
                    cur.execute("DELETE FROM " + tabela)
                cur.executemany("INSERT INTO produtos (produto_id,nome,categoria,preco_base) VALUES (%s,%s,%s,%s)", [
                    (p["produto_id"], p["nome"], p["categoria"], p["preco_base"]) for p in dados["produtos"]])
                cur.executemany("INSERT INTO clientes (id,nome,email,cidade,estado,cadastro_em) VALUES (%s,%s,%s,%s,%s,%s)", [
                    (c["id"], c["nome"], c["email"], c["cidade"], c["estado"], c["cadastro_em"])
                    for c in dados["clientes"]])
                for p in dados["pedidos"]:
                    cur.execute("INSERT INTO pedidos (id,cliente_id,data_pedido,status,valor_total,valor_itens,divergente) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (p["id"], p["cliente_id"], p["data_pedido"], p["status"], p["valor_total"], p["valor_itens"], p["divergente"]))
                    cur.executemany("INSERT INTO itens_pedido (pedido_id,linha,produto_id,quantidade,preco_unitario) VALUES (%s,%s,%s,%s,%s)", [
                        (p["id"], i, item["produto_id"], item["quantidade"], item["preco_unitario"])
                        for i, item in enumerate(p["itens"], 1)])
        return conexao
    except Exception:
        conexao.close()
        raise
