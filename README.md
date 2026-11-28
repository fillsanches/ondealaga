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

O comando inicia a API e o PostgreSQL com PostGIS em segundo plano e
aguarda a checagem de prontidão do banco. A API estará disponível em
`http://localhost:8000`.
O endpoint `GET /healthz` retorna `{"status":"ok"}`.

### Banco de desenvolvimento

Com os serviços em execução, confira a extensão PostGIS no banco:

```bash
docker compose exec db psql -U onde_alaga -d onde_alaga -c "SELECT PostGIS_Version();"
```

O banco usa um volume persistente e fica na rede interna do Compose. A
imagem do PostGIS é `linux/amd64`. Em máquinas ARM, o Docker precisa de
suporte à emulação dessa arquitetura.

Com os serviços em execução, aplique as migrações e confira a revisão:

```bash
docker compose exec api uv run --locked --no-dev alembic upgrade head
docker compose exec api uv run --locked --no-dev alembic current
```

## Contribuir

Abra uma issue para relatar um problema, sugerir uma melhoria ou indicar
uma fonte de dados. Para mudanças no código, envie um pull request e
vincule a issue correspondente, quando houver.

Antes de enviar um pull request, rode as verificações na raiz do projeto:

```bash
docker compose run --rm checks
```

O comando verifica lint, formatação do Python e testes em um contêiner
temporário. No PR, o GitHub Actions também executa essas verificações e
aplica as migrações em um banco PostGIS novo para validar o esquema.

## Licença

O código é distribuído sob a [licença MIT](LICENSE). Os dados de terceiros
seguem as condições de uso das respectivas fontes.
