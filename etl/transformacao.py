# -*- coding: utf-8 -*-
"""Transformacoes puras do ETL Verdejar."""
import datetime
from copy import deepcopy
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENTAVO = Decimal("0.01")


def normalizar_email(cliente):
    """A1: preserva email ausente como None e limpa espaços."""
    cliente = dict(cliente)
    email = cliente.get("email")
    if email is None or not str(email).strip():
        cliente["email"] = None
        return cliente, 1
    cliente["email"] = str(email).strip()
    return cliente, 0


def normalizar_estado(cliente):
    """A2: sigla de estado em duas letras maiusculas."""
    cliente = dict(cliente)
    original = str(cliente["estado"]).strip()
    cliente["estado"] = original.upper()
    if len(cliente["estado"]) != 2:
        raise ValueError("estado deve conter exatamente duas letras")
    return cliente, int(original != cliente["estado"])


def converter_data_pedido(pedido):
    """A3: aceita AAAA-MM-DD e DD/MM/AAAA e entrega ISO 8601."""
    pedido = dict(pedido)
    valor = pedido["data_pedido"]
    convertido = "/" in valor
    try:
        data = datetime.datetime.strptime(valor, "%Y-%m-%d").date()
    except ValueError:
        data = datetime.datetime.strptime(valor, "%d/%m/%Y").date()
    pedido["data_pedido"] = data.isoformat()
    return pedido, int(convertido)


def converter_valor_total(pedido):
    """A4: converte numero ou texto decimal com virgula para centavos."""
    pedido = dict(pedido)
    valor = pedido["valor_total"]
    convertido = isinstance(valor, str)
    if isinstance(valor, str):
        valor = valor.strip()
        if "," in valor:
            # Ponto antes da vírgula é separador de milhar; vírgula é decimal.
            valor = valor.replace(".", "").replace(",", ".")
    try:
        pedido["valor_total"] = Decimal(str(valor)).quantize(CENTAVO, rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        raise ValueError("valor_total invalido: {!r}".format(valor))
    return pedido, int(convertido)


def deduplicar_pedidos(pedidos):
    """A5: mantém a primeira ocorrência de cada id e contabiliza descartes."""
    vistos, unicos = set(), []
    repetidos = 0
    for pedido in pedidos:
        pid = pedido["id"]
        if pid in vistos:
            repetidos += 1
            continue
        vistos.add(pid)
        unicos.append(dict(pedido))
    return unicos, repetidos


def calcular_valor_itens(pedido):
    """A6: calcula o total dos itens e marca divergencia acima de um centavo."""
    pedido = dict(pedido)
    total = sum((Decimal(str(item["quantidade"])) * Decimal(str(item["preco_unitario"]))
                 for item in pedido["itens"]), Decimal("0"))
    pedido["valor_itens"] = total.quantize(CENTAVO, rounding=ROUND_HALF_UP)
    pedido["divergente"] = abs(pedido["valor_total"] - pedido["valor_itens"]) > CENTAVO
    return pedido, 1


def transformar(clientes, pedidos, produtos):
    # Copia profundamente para manter a transformação livre de efeitos colaterais
    # inclusive nos dicionários aninhados de itens de pedido.
    clientes = deepcopy(clientes)
    pedidos = deepcopy(pedidos)
    produtos = deepcopy(produtos)
    cont = {"emails_nulos": 0, "estados_padronizados": 0, "datas_convertidas": 0,
            "valores_convertidos": 0, "pedidos_repetidos_descartados": 0,
            "pedidos_divergentes": 0}
    clientes_tratados = []
    for cliente in clientes:
        cliente, n = normalizar_email(cliente); cont["emails_nulos"] += n
        cliente, n = normalizar_estado(cliente); cont["estados_padronizados"] += n
        clientes_tratados.append(cliente)
    pedidos, cont["pedidos_repetidos_descartados"] = deduplicar_pedidos(pedidos)
    pedidos_tratados = []
    for pedido in pedidos:
        pedido, n = converter_data_pedido(pedido); cont["datas_convertidas"] += n
        pedido, n = converter_valor_total(pedido); cont["valores_convertidos"] += n
        pedido, n = calcular_valor_itens(pedido)
        cont["pedidos_divergentes"] += int(pedido["divergente"])
        pedidos_tratados.append(pedido)
    return {"clientes": clientes_tratados, "produtos": produtos, "pedidos": pedidos_tratados}, cont
