# Onde Alaga

## Mapa público e colaborativo para consultar o histórico de alagamentos no Brasil

O Onde Alaga é um projeto de código aberto para consultar o histórico de
alagamentos no Brasil antes de escolher onde morar. A proposta é reunir
ocorrências por local e período, com links para as fontes originais.

## Executar localmente

Requisitos: Docker com Compose.

```bash
docker compose up -d --build --wait
```

O Compose aguarda o PostgreSQL com PostGIS, aplica as migrações pendentes
e inicia a API. Quando o comando termina com sucesso, a API está disponível
em `http://localhost:8000`, com `GET /healthz` retornando `{"status":"ok"}`.

O banco usa um volume persistente e fica na rede interna do Compose. A
imagem do PostGIS é `linux/amd64`. Em máquinas ARM, o Docker precisa de
suporte à emulação dessa arquitetura.

### Enviar uma proposta para revisão

Com o Compose em execução, use o comando interno abaixo com os IDs de uma
localidade e de uma fonte já cadastradas no banco de desenvolvimento:

```bash
docker compose exec api .venv/bin/python -m app.submit_proposal --locality-id 1 --event-type flood --year 2026 --month 3 --evidence 1 https://example.org/boletim
```

Informe apenas os componentes de data conhecidos. A opção `--evidence`
pode ser omitida ou repetida para acrescentar evidências. O comando salva
a proposta como pendente e imprime seu identificador.

## Contribuir

Abra uma issue para relatar um problema, sugerir uma melhoria ou indicar
uma fonte de dados. Para mudanças no código, envie um pull request e
vincule a issue correspondente, quando houver.

Antes de enviar um pull request, rode as verificações na raiz do projeto:

```bash
docker compose run --rm checks
```

O comando inicia um PostGIS separado, verifica lint e formatação, aplica
as migrações pendentes, confirma que o esquema está na revisão mais recente
e roda os testes. Basta ter o Docker em execução, mesmo em um clone novo.
O banco de verificações pode ser reutilizado enquanto estiver ativo. Seus
dados temporários são descartados ao parar `docker compose stop checks-db`.
O GitHub Actions usa a mesma rotina com um banco novo e também valida a
subida da API.

## Licença

O código é distribuído sob a [licença MIT](LICENSE). Os dados de terceiros
seguem as condições de uso das respectivas fontes.
