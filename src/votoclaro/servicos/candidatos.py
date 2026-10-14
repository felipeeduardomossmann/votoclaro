"""Servico de Candidatos: regras de busca e montagem da ficha."""

from votoclaro.repositorio import RepositorioCandidatos


class ServicoCandidatos:
    def __init__(self, repositorio: RepositorioCandidatos) -> None:
        self._repositorio = repositorio

    def buscar(self, cidade: str | None = None, cargo: str | None = None) -> list[dict]:
        """Filtra por cidade e cargo. A ordem e sempre alfabetica, por neutralidade."""
        resultado = self._repositorio.listar()
        if cidade:
            resultado = [c for c in resultado if c["cidade"].lower() == cidade.lower()]
        if cargo:
            resultado = [c for c in resultado if c["cargo"].lower() == cargo.lower()]
        return sorted(resultado, key=lambda c: c["nome"])

    def ficha(self, candidato_id: int) -> dict | None:
        candidato = self._repositorio.buscar_por_id(candidato_id)
        if candidato is None:
            return None
        return {
            "id": candidato["id"],
            "nome": candidato["nome"],
            "partido": candidato["partido"],
            "cargo": candidato["cargo"],
            "cidade": f"{candidato['cidade']}/{candidato['uf']}",
            "situacao": candidato["situacao"],
            "bens_declarados": candidato["bens_declarados"],
            "propostas": candidato["propostas"],
            "fonte": "Portal de Dados Abertos do TSE",
        }

    def posicoes(self) -> list[dict]:
        """Posicoes usadas pelo teste de afinidade, calculado no navegador (ADR 002)."""
        return [
            {"id": c["id"], "nome": c["nome"], "posicoes": c["posicoes"]} for c in self.buscar()
        ]
