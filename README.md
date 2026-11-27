# Onde Alaga

## Mapa público e colaborativo para consultar o histórico de alagamentos no Brasil

O Onde Alaga é um projeto de código aberto para consultar o histórico de
alagamentos no Brasil antes de escolher onde morar. A proposta é reunir
ocorrências por local e período, com links para as fontes originais.

## Executar localmente

Requisitos: Docker com Compose.

```bash
docker compose up --build
```

A API estará disponível em `http://localhost:8000`.
O endpoint `GET /healthz` retorna `{"status":"ok"}`.

## Contribuir

Abra uma issue para relatar um problema, sugerir uma melhoria ou indicar
uma fonte de dados. Para mudanças no código, envie um pull request e
vincule a issue correspondente, quando houver.

Antes de enviar um pull request, rode as verificações na raiz do projeto:

```bash
docker compose run --rm checks
```

O comando verifica lint, formatação do Python e testes em um contêiner
temporário. O GitHub Actions também executa essas verificações no PR.

## Licença

O código é distribuído sob a [licença MIT](LICENSE). Os dados de terceiros
seguem as condições de uso das respectivas fontes.
