import pytest

from votoclaro.repositorio import RepositorioCandidatos
from votoclaro.servicos.candidatos import ServicoCandidatos
from votoclaro.servicos.comparacao import SEM_PROPOSTA, ServicoComparacao


@pytest.fixture
def candidatos():
    return ServicoCandidatos(RepositorioCandidatos())


def test_busca_filtra_por_cidade_e_cargo(candidatos):
    resultado = candidatos.buscar(cidade="Vale Verde", cargo="prefeito")
    assert [c["nome"] for c in resultado] == ["Ana Ribeiro", "Bruno Carvalho"]


def test_busca_ignora_maiusculas(candidatos):
    assert len(candidatos.buscar(cidade="vale verde")) == 3


def test_busca_sempre_em_ordem_alfabetica(candidatos):
    nomes = [c["nome"] for c in candidatos.buscar()]
    assert nomes == sorted(nomes)


def test_ficha_mostra_a_fonte_oficial(candidatos):
    ficha = candidatos.ficha(1)
    assert ficha["cidade"] == "Vale Verde/RS"
    assert ficha["fonte"] == "Portal de Dados Abertos do TSE"


def test_ficha_de_candidato_inexistente(candidatos):
    assert candidatos.ficha(999) is None


def test_posicoes_nao_carregam_dados_do_eleitor(candidatos):
    for item in candidatos.posicoes():
        assert set(item) == {"id", "nome", "posicoes"}


def test_comparacao_alinha_temas(candidatos):
    resultado = ServicoComparacao(candidatos).comparar([1, 3])
    assert resultado["temas"]["educacao"]["Carla Souza"].startswith("Propor merenda")
    assert resultado["temas"]["saude"]["Carla Souza"] == SEM_PROPOSTA


def test_comparacao_exige_dois_candidatos(candidatos):
    with pytest.raises(ValueError):
        ServicoComparacao(candidatos).comparar([1])


def test_comparacao_com_candidato_inexistente(candidatos):
    with pytest.raises(LookupError):
        ServicoComparacao(candidatos).comparar([1, 999])
