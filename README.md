# VotoClaro

![CI](https://github.com/SEU_USUARIO/votoclaro/actions/workflows/ci.yml/badge.svg)

API do VotoClaro, um app para o eleitor se informar antes de votar usando apenas dados oficiais do TSE e de forma neutra.

> Os dados de candidatos deste repositório são fictícios e servem apenas para desenvolvimento e testes.

A documentação completa (acordos de trabalho, arquitetura C4 e ADRs) está na [Wiki](../../wiki).

## Processo de build

O build usa o **Nox** para definir as tasks e o **GitHub Actions** como servidor de integração contínua. Ele roda automaticamente a cada envio para a `main` e a cada pull request.

| Ordem | Task | O que faz | Quando falha |
|---|---|---|---|
| 1 | `lint` | Verifica estilo, erros comuns e formatação com o Ruff | Código fora do padrão PEP 8 ou com erro óbvio |
| 2 | `testes` | Roda os testes com pytest e mede a cobertura | Algum teste falha ou a cobertura fica abaixo de 80% |
| 3 | `build` | Gera o pacote instalável em `dist/` | O pacote não pode ser montado |

Se uma task falha, as seguintes não rodam. Ao final, o pacote e os relatórios de testes ficam disponíveis para download na execução do Actions.

## Rodar no seu computador

```bash
pip install nox
nox            # roda as três tasks
nox -s testes  # roda só uma
```

Para subir a API e ver a documentação interativa em http://127.0.0.1:8000/docs:

```bash
pip install -e ".[dev]" uvicorn
uvicorn votoclaro.main:app --reload
```

## Estrutura

```
src/votoclaro/
  main.py            ponto de entrada da API
  rotas.py           rotas de candidatos, comparação, questionário e explicador
  servicos/          regras de negócio
  repositorio.py     acesso aos dados
  dados/             dados fictícios
tests/               testes automatizados
noxfile.py           definição das tasks do build
.github/workflows/   configuração do servidor de CI
```
