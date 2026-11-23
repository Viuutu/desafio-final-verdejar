# -*- coding: utf-8 -*-
from copy import deepcopy
from decimal import Decimal

from etl.transformacao import (calcular_valor_itens, converter_data_pedido,
    converter_valor_total, deduplicar_pedidos, normalizar_email, normalizar_estado,
    transformar)


def test_a1_email_ausente_permanece_nulo():
    cliente, n = normalizar_email({"email": None})
    assert cliente["email"] is None and n == 1


def test_a2_estado_vai_para_maiusculas():
    cliente, _ = normalizar_estado({"estado": "rS"})
    assert cliente["estado"] == "RS"


def test_a3_data_dia_mes_ano_vira_iso():
    pedido, _ = converter_data_pedido({"data_pedido": "19/02/2026"})
    assert pedido["data_pedido"] == "2026-02-19"


def test_a4_valor_decimal_com_virgula():
    pedido, _ = converter_valor_total({"valor_total": "125,84"})
    assert pedido["valor_total"] == Decimal("125.84")


def test_a4_valor_textual_com_ponto_decimal_nao_multiplica_por_cem():
    pedido, _ = converter_valor_total({"valor_total": "125.84"})
    assert pedido["valor_total"] == Decimal("125.84")


def test_a5_pedido_repetido_descarta_segunda_ocorrencia():
    primeira = {"id": 1, "v": "primeiro"}
    unicos, repetidos = deduplicar_pedidos([primeira, {"id": 1, "v": "repetido"}])
    assert unicos == [primeira] and repetidos == 1


def test_a6_soma_itens_e_marca_divergencia():
    pedido = {"valor_total": Decimal("10.00"), "itens": [
        {"quantidade": 2, "preco_unitario": 3.0}, {"quantidade": 1, "preco_unitario": 4.0}]}
    pedido, _ = calcular_valor_itens(pedido)
    assert pedido["valor_itens"] == Decimal("10.00")
    assert pedido["divergente"] is False


def test_a6_diferenca_maior_que_centavo_e_divergente():
    pedido = {"valor_total": Decimal("11.00"), "itens": [{"quantidade": 1, "preco_unitario": 10.0}]}
    pedido, _ = calcular_valor_itens(pedido)
    assert pedido["divergente"] is True


def test_funcoes_de_transformacao_nao_alteram_os_registros_de_entrada():
    cliente = {"email": None, "estado": "rs"}
    pedido = {"id": 1, "data_pedido": "01/01/2026", "valor_total": "10,00",
              "itens": [{"quantidade": 2, "preco_unitario": 5.0}]}
    clientes = [cliente]
    pedidos = [pedido]
    produtos = [{"produto_id": 1, "nome": "P", "categoria": "frutas", "preco_base": 5.0}]
    originais = deepcopy((clientes, pedidos, produtos))

    transformar(clientes, pedidos, produtos)

    assert (clientes, pedidos, produtos) == originais
