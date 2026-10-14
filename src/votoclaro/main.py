"""Ponto de entrada da API do VotoClaro."""

from fastapi import FastAPI

from votoclaro import __version__
from votoclaro.rotas import (
    rotas_candidatos,
    rotas_comparacao,
    rotas_explicador,
    rotas_questionario,
)

app = FastAPI(title="VotoClaro API", version=__version__)

app.include_router(rotas_candidatos)
app.include_router(rotas_comparacao)
app.include_router(rotas_questionario)
app.include_router(rotas_explicador)


@app.get("/saude", tags=["Monitoramento"])
def saude():
    return {"status": "ok", "versao": __version__}
