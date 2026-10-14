"""Repositorio: unica parte da API que conhece a origem dos dados.

Nesta primeira versao os dados vem de um arquivo JSON ficticio.
Quando o PostgreSQL entrar (ADR 003), so esta classe muda.
"""

import json
from importlib import resources


class RepositorioCandidatos:
    def __init__(self, dados: dict | None = None) -> None:
        if dados is None:
            arquivo = resources.files("votoclaro.dados").joinpath("candidatos.json")
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
        self._candidatos = dados["candidatos"]
        self._perguntas = dados["perguntas"]

    def listar(self) -> list[dict]:
        return list(self._candidatos)

    def buscar_por_id(self, candidato_id: int) -> dict | None:
        return next((c for c in self._candidatos if c["id"] == candidato_id), None)

    def listar_perguntas(self) -> list[dict]:
        return list(self._perguntas)
