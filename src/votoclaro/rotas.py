"""Rotas da API, uma para cada funcionalidade do C4 nivel 3."""

from fastapi import APIRouter, HTTPException, Query

from votoclaro.repositorio import RepositorioCandidatos
from votoclaro.servicos.candidatos import ServicoCandidatos
from votoclaro.servicos.comparacao import ServicoComparacao
from votoclaro.servicos.quociente import quociente_eleitoral, quociente_partidario

repositorio = RepositorioCandidatos()
servico_candidatos = ServicoCandidatos(repositorio)
servico_comparacao = ServicoComparacao(servico_candidatos)

rotas_candidatos = APIRouter(prefix="/candidatos", tags=["Candidatos"])
rotas_comparacao = APIRouter(prefix="/comparacao", tags=["Comparacao"])
rotas_questionario = APIRouter(prefix="/questionario", tags=["Questionario"])
rotas_explicador = APIRouter(prefix="/explicador", tags=["Explicador da urna"])


@rotas_candidatos.get("")
def buscar_candidatos(cidade: str | None = None, cargo: str | None = None):
    return servico_candidatos.buscar(cidade, cargo)


@rotas_candidatos.get("/{candidato_id}")
def ficha_do_candidato(candidato_id: int):
    ficha = servico_candidatos.ficha(candidato_id)
    if ficha is None:
        raise HTTPException(status_code=404, detail="Candidato nao encontrado")
    return ficha


@rotas_comparacao.get("")
def comparar_candidatos(ids: list[int] = Query(...)):
    try:
        return servico_comparacao.comparar(ids)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro
    except LookupError as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from erro


@rotas_questionario.get("")
def questionario():
    return {
        "perguntas": repositorio.listar_perguntas(),
        "candidatos": servico_candidatos.posicoes(),
    }


@rotas_explicador.get("/quociente")
def explicar_quociente(votos_validos: int, vagas: int, votos_partido: int = 0):
    try:
        qe = quociente_eleitoral(votos_validos, vagas)
        return {
            "quociente_eleitoral": qe,
            "vagas_do_partido": quociente_partidario(votos_partido, qe) if qe else 0,
        }
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro
