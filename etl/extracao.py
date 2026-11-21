# -*- coding: utf-8 -*-
"""Cliente HTTP paginado e preservacao de dados brutos."""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


class ErroExtracao(RuntimeError):
    pass


def consumir_rota(base_url, rota, page_size=200, timeout=15):
    pagina, paginas, todos, registros = 1, None, [], 0
    while paginas is None or pagina <= paginas:
        url = "{}/{}?{}".format(base_url.rstrip("/"), rota,
                                 urlencode({"page": pagina, "page_size": page_size}))
        try:
            with urlopen(url, timeout=timeout) as resposta:
                if resposta.status != 200:
                    raise ErroExtracao("HTTP {} ao consultar {} pagina {}".format(resposta.status, rota, pagina))
                payload = json.loads(resposta.read().decode("utf-8"))
        except HTTPError as exc:
            raise ErroExtracao("HTTP {} ao consultar {} pagina {}".format(exc.code, rota, pagina))
        except (URLError, OSError) as exc:
            raise ErroExtracao("Falha de conexao ao consultar {} pagina {}: {}".format(rota, pagina, exc))
        except ValueError as exc:
            raise ErroExtracao("JSON invalido em {} pagina {}: {}".format(rota, pagina, exc))
        todos.extend(payload.get("items", []))
        registros += len(payload.get("items", []))
        paginas = payload.get("total_pages")
        pagina += 1
    return todos, {"paginas": paginas or 0, "registros": registros}


def salvar_bruto(diretorio, nome, dados):
    os.makedirs(diretorio, exist_ok=True)
    caminho = os.path.join(diretorio, nome + ".json")
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
    return caminho
