import pytest

from votoclaro.servicos.quociente import quociente_eleitoral, quociente_partidario


@pytest.mark.parametrize(
    ("votos", "vagas", "esperado"),
    [
        (10000, 9, 1111),  # fracao menor que meio e desprezada
        (10000, 3, 3333),  # fracao de um terco tambem
        (10007, 9, 1112),  # fracao maior que meio vira um
        (900, 9, 100),  # divisao exata
    ],
)
def test_quociente_eleitoral(votos, vagas, esperado):
    assert quociente_eleitoral(votos, vagas) == esperado


def test_quociente_partidario_despreza_fracao():
    assert quociente_partidario(2500, 1111) == 2


def test_vagas_invalidas():
    with pytest.raises(ValueError):
        quociente_eleitoral(1000, 0)


def test_votos_negativos():
    with pytest.raises(ValueError):
        quociente_eleitoral(-1, 9)


def test_quociente_invalido():
    with pytest.raises(ValueError):
        quociente_partidario(100, 0)
