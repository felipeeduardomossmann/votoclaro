"""Calculos do explicador da urna para eleicoes proporcionais (vereador)."""


def quociente_eleitoral(votos_validos: int, vagas: int) -> int:
    """Votos validos divididos pelas vagas, arredondando como manda a lei.

    Fracao igual ou menor que meio e desprezada, maior que meio vira um.
    """
    if vagas <= 0:
        raise ValueError("O numero de vagas deve ser positivo")
    if votos_validos < 0:
        raise ValueError("Os votos validos nao podem ser negativos")
    inteiro, resto = divmod(votos_validos, vagas)
    return inteiro + 1 if resto * 2 > vagas else inteiro


def quociente_partidario(votos_partido: int, quociente: int) -> int:
    """Quantas vagas o partido conquista direto, desprezando a fracao."""
    if quociente <= 0:
        raise ValueError("O quociente eleitoral deve ser positivo")
    return votos_partido // quociente
