"""Tasks do build do VotoClaro.

Rode `nox` para executar todas, na ordem, ou `nox -s testes` para uma so.
"""

import nox

nox.options.sessions = ["lint", "testes", "build"]
nox.options.reuse_existing_virtualenvs = True


@nox.session
def lint(session):
    """Task 1: verifica estilo, erros comuns e formatacao do codigo."""
    session.install("ruff")
    session.run("ruff", "check", "src", "tests", "noxfile.py")
    session.run("ruff", "format", "--check", "src", "tests", "noxfile.py")


@nox.session
def testes(session):
    """Task 2: roda os testes e exige pelo menos 80% de cobertura."""
    session.install("-e", ".[dev]")
    session.run(
        "pytest",
        "--cov",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "--cov-fail-under=80",
        "--junitxml=relatorio-testes.xml",
    )


@nox.session
def build(session):
    """Task 3: gera o pacote instalavel (.whl) e o pacote de codigo (.tar.gz)."""
    session.install("build")
    session.run("python", "-m", "build")
