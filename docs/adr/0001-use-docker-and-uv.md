# ADR 0001 — Executar a API com Docker e gerenciar dependências com uv

## Status

Aceito.

## Contexto

O desenvolvimento começou no Windows com o Zed, e o CI roda em Linux. 
O projeto precisa de uma forma reproduzível de instalar as dependências Python
e executar a API em ambientes de desenvolvimento Windows, Linux e macOS.

## Decisão

Usar Docker Compose para executar os serviços locais e uv para gerenciar
as dependências no `pyproject.toml` e no `uv.lock`. Versionar o lockfile
e usar `uv sync --locked --no-dev` na imagem da API.

## Consequências

O comando geral do Compose inicia a API e o banco de desenvolvimento
definido no ADR 0002. O build falha se o lockfile estiver fora de
sincronia com o `pyproject.toml`. Alterações de dependências exigem
atualizar os dois arquivos no mesmo PR.
