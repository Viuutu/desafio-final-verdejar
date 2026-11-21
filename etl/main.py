# -*- coding: utf-8 -*-
"""Orquestracao do ETL. Compatível com Python 3.8+."""
import argparse
import csv
import json
import os
import sqlite3
import sys

try:  # execucao como modulo
    from .extracao import ErroExtracao, consumir_rota, salvar_bruto
    from .transformacao import transformar
    from .carga import carregar_postgres, carregar_sqlite
except ImportError:  # execucao direta: python etl/main.py
    from extracao import ErroExtracao, consumir_rota, salvar_bruto
    from transformacao import transformar
    from carga import carregar_postgres, carregar_sqlite


def ler_produtos(caminho):
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        return [{"produto_id": int(r["produto_id"]), "nome": r["nome"], "categoria": r["categoria"],
                 "preco_base": float(r["preco_base"])} for r in csv.DictReader(arquivo)]


def executar(args):
    if args.reprocessar:
        with open(os.path.join(args.brutos, "clientes.json"), encoding="utf-8") as f: clientes = json.load(f)
        with open(os.path.join(args.brutos, "pedidos.json"), encoding="utf-8") as f: pedidos = json.load(f)
        metadados = {"clientes": {"paginas": 0, "registros": len(clientes)}, "pedidos": {"paginas": 0, "registros": len(pedidos)}}
    else:
        try:
            clientes, mc = consumir_rota(args.api, "clientes", args.page_size)
            salvar_bruto(args.brutos, "clientes", clientes)
            pedidos, mp = consumir_rota(args.api, "pedidos", args.page_size)
            salvar_bruto(args.brutos, "pedidos", pedidos)
            metadados = {"clientes": mc, "pedidos": mp}
        except ErroExtracao as exc:
            print("erro: {}".format(exc), file=sys.stderr)
            return 2
    produtos = ler_produtos(args.produtos)
    dados, cont = transformar(clientes, pedidos, produtos)
    print("extracao: clientes paginas={} registros={}".format(metadados["clientes"]["paginas"], metadados["clientes"]["registros"]))
    print("extracao: pedidos paginas={} registros={}".format(metadados["pedidos"]["paginas"], metadados["pedidos"]["registros"]))
    print("transformacao: pedidos_unicos={} repetidos_descartados={}".format(len(dados["pedidos"]), cont["pedidos_repetidos_descartados"]))
    print("transformacao: emails_nulos={} estados_padronizados={} datas_convertidas={}".format(cont["emails_nulos"], cont["estados_padronizados"], cont["datas_convertidas"]))
    print("transformacao: valores_convertidos={} pedidos_divergentes={}".format(cont["valores_convertidos"], cont["pedidos_divergentes"]))
    if args.banco == "sqlite":
        db = carregar_sqlite(args.sqlite, dados, args.schema_sqlite)
    else:
        db = carregar_postgres(args.dsn, dados)
    try:
        c = db.cursor()
        counts = {t: c.execute("SELECT COUNT(*) FROM " + t).fetchone()[0]
                  for t in ("clientes", "produtos", "pedidos", "itens_pedido")}
        origem = sum(float(p["valor_itens"]) for p in dados["pedidos"])
        destino = c.execute("SELECT COALESCE(SUM(valor_itens),0) FROM pedidos").fetchone()[0]
        dif = abs(origem - float(destino))
        print("carga: clientes={} produtos={} pedidos={} itens={}".format(counts["clientes"], counts["produtos"], counts["pedidos"], counts["itens_pedido"]))
        print("reconciliacao: soma_valor_itens_origem={:.2f} soma_valor_itens_destino={:.2f} diferenca={:.2f}".format(origem, float(destino), dif))
        print("divergentes: {} pedidos com valor_total diferente da soma dos itens".format(cont["pedidos_divergentes"]))
        return 0 if dif <= 0.01 else 1
    finally:
        db.close()


def main():
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--api", default="http://127.0.0.1:8000")
    ap.add_argument("--page-size", type=int, default=200)
    ap.add_argument("--brutos", default=os.path.join(raiz, "brutos"))
    ap.add_argument("--reprocessar", action="store_true")
    ap.add_argument("--banco", choices=("postgres", "sqlite"), default="sqlite")
    ap.add_argument("--sqlite", default=os.path.join(raiz, "verdejar.db"))
    ap.add_argument("--dsn", default=os.environ.get("VERDEJAR_DSN", "dbname=verdejar user=postgres password=postgres host=localhost port=5432"))
    ap.add_argument("--produtos", default=os.path.join(raiz, "insumos", "dados", "produtos.csv"))
    ap.add_argument("--schema-sqlite", default=os.path.join(raiz, "insumos", "schema_sqlite.sql"))
    sys.exit(executar(ap.parse_args()))


if __name__ == "__main__": main()
