"""Servico de Comparacao: alinha as propostas dos candidatos por tema."""

from votoclaro.servicos.candidatos import ServicoCandidatos

SEM_PROPOSTA = "Sem proposta registrada para este tema"


class ServicoComparacao:
    def __init__(self, servico_candidatos: ServicoCandidatos) -> None:
        self._candidatos = servico_candidatos

    def comparar(self, ids: list[int]) -> dict:
        if len(ids) < 2:
            raise ValueError("Informe pelo menos dois candidatos para comparar")

        fichas = [self._candidatos.ficha(i) for i in ids]
        if any(f is None for f in fichas):
            raise LookupError("Candidato nao encontrado")

        temas = sorted({tema for f in fichas for tema in f["propostas"]})
        return {
            "candidatos": [f["nome"] for f in fichas],
            "temas": {
                tema: {f["nome"]: f["propostas"].get(tema, SEM_PROPOSTA) for f in fichas}
                for tema in temas
            },
        }
