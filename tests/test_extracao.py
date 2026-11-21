import json
from unittest.mock import patch

from etl.extracao import consumir_rota, ErroExtracao


class Resposta:
    status = 200
    def __init__(self, pagina): self.pagina = pagina
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self):
        items = [{"id": self.pagina}]
        return json.dumps({"items": items, "total_pages": 2}).encode("utf-8")


def test_paginacao_consume_todas_as_paginas():
    def fake_urlopen(url, timeout):
        return Resposta(2 if "page=2" in url else 1)
    with patch("etl.extracao.urlopen", side_effect=fake_urlopen):
        dados, cont = consumir_rota("http://api-teste", "pedidos", page_size=1)
    assert dados == [{"id": 1}, {"id": 2}]
    assert cont == {"paginas": 2, "registros": 2}
