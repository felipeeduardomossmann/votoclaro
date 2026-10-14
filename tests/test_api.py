from fastapi.testclient import TestClient

from votoclaro.main import app

cliente = TestClient(app)


def test_saude():
    assert cliente.get("/saude").json()["status"] == "ok"


def test_buscar_candidatos():
    resposta = cliente.get("/candidatos", params={"cidade": "Serra Alta"})
    assert resposta.status_code == 200
    assert resposta.json()[0]["nome"] == "Diego Martins"


def test_ficha_inexistente_retorna_404():
    assert cliente.get("/candidatos/999").status_code == 404


def test_ficha_existente():
    assert cliente.get("/candidatos/2").json()["nome"] == "Bruno Carvalho"


def test_comparacao():
    resposta = cliente.get("/comparacao", params={"ids": [1, 2]})
    assert resposta.status_code == 200
    assert set(resposta.json()["temas"]) == {"educacao", "saude", "seguranca"}


def test_comparacao_com_um_candidato_retorna_400():
    assert cliente.get("/comparacao", params={"ids": [1]}).status_code == 400


def test_comparacao_com_inexistente_retorna_404():
    assert cliente.get("/comparacao", params={"ids": [1, 999]}).status_code == 404


def test_questionario_entrega_perguntas_e_posicoes():
    dados = cliente.get("/questionario").json()
    assert len(dados["perguntas"]) == 3
    assert len(dados["candidatos"]) == 4


def test_explicador_quociente():
    params = {"votos_validos": 10000, "vagas": 9, "votos_partido": 2500}
    dados = cliente.get("/explicador/quociente", params=params).json()
    assert dados == {"quociente_eleitoral": 1111, "vagas_do_partido": 2}


def test_explicador_com_vagas_invalidas_retorna_400():
    params = {"votos_validos": 10000, "vagas": 0}
    assert cliente.get("/explicador/quociente", params=params).status_code == 400
