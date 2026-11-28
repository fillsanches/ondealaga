# ADR 0003 - Concentrar as regras de negócio no domínio

## Status

Aceito.

## Contexto

Consultas públicas, relatos da comunidade e dados de fontes externas
precisam seguir as mesmas regras de cobertura, verificação e contagem, mesmo
quando chegam por interfaces diferentes.

## Decisão

- **Domínio (`app/domain/`):** implementar em Python as regras que definem
  o comportamento do produto. A classificação da cobertura usa apenas
  datas e pode ser testada isoladamente. As regras de verificação, contagem
  e reputação entram nesse domínio quando seus casos de uso forem entregues.
- **Aplicação (`app/application/`):** criar os casos de uso à medida que
  forem necessários. Um caso de uso de revisão consulta os dados, valida
  a permissão editorial, aplica a regra de domínio e registra a decisão
  na mesma transação em que atualiza a ocorrência.
- **Interface (FastAPI e mapa):** receber entradas, validar formato e
  apresentar o resultado do caso de uso. O mapa exibe os estados e totais
  retornados pelo servidor.
- **Infraestrutura:** integrar PostGIS, geocodificação e armazenamento de
  arquivos. O banco garante chaves, unicidade e integridade, como um fim
  de cobertura igual ou posterior ao início. Consultas SQL podem fazer
  agregações a partir dos critérios definidos pelo domínio.

## Consequências

O domínio depende da biblioteca padrão. Validações que protegem a
integridade dos dados também podem ser garantidas pelo banco. Adicionar
casos de uso e adaptadores conforme tenham um consumidor concreto.
