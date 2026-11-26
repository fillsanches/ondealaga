# ADR 0001 — Executar a API com Docker e gerenciar dependências com uv

## Status

Aceito.

## Contexto

O ambiente de desenvolvimento inicial usa Windows com Zed, e o CI roda em
Linux. O projeto precisa de um modo reproduzível de subir a API e instalar
as dependências Python.

## Decisão

Usar Docker Compose para executar a API localmente e uv para gerenciar as
dependências no `pyproject.toml` e no `uv.lock`. Versionar o lockfile e usar
`uv sync --locked --no-dev` na imagem da API.

## Consequências

O mesmo comando de Compose sobe a API em máquinas com Docker. O build
falha se o lockfile estiver fora de sincronia com o `pyproject.toml`.
Alterações de dependências exigem atualizar os dois arquivos no mesmo PR.
