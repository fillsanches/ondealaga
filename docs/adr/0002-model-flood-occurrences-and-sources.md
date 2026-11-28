# ADR 0002 — Modelar ocorrências e fontes para múltiplos países

## Status

Aceito para o M1.

## Contexto

O Onde Alaga começa no Brasil. Precisamos representar ocorrências históricas
com a precisão disponível e rastrear as fontes que sustentam cada registro.
O modelo também precisa acomodar países com divisões administrativas e
sistemas de identificação próprios.

## Decisão

Usar PostgreSQL como banco relacional. Chaves estrangeiras mantêm os vínculos
entre localidades, ocorrências, fontes e evidências. A extensão PostGIS dá
suporte às consultas espaciais, como buscar ocorrências próximas a um endereço.

Incluir o banco de desenvolvimento na subida padrão do Docker Compose e
persistir os dados em um volume. As mudanças de esquema serão versionadas
com Alembic a partir da primeira migração.

Usar nomes de campos em inglês no código e no esquema de dados. Os valores
preservam a grafia local, como `São Paulo`. Cada país fornece o mapeamento
entre seus dados de origem e os conceitos abaixo.

### Localidade (`Locality`)

Unidade territorial usada para vincular ocorrências e organizar páginas
públicas. Tem identificador interno (`id`), nome (`name`) e código de país
(`country_code`). O código da divisão administrativa (`subdivision_code`)
é opcional. Cada localidade pode ter identificadores externos, registrados
com o país, o sistema de identificação e o valor. Os códigos externos são
tratados como texto para preservar zeros à esquerda e formatos alfanuméricos.

No Brasil, um município pode ter `name = "São Paulo"`, `country_code = "BR"`,
`subdivision_code = "SP"` e um identificador externo do sistema `IBGE`. A sigla
da UF preenche o campo de divisão administrativa, e o código IBGE é um dado
do catálogo brasileiro. Outros países podem informar seus próprios códigos.

### Ocorrência (`Occurrence`)

Evento registrado, como um alagamento. Guarda o tipo do evento, a localidade,
a data da ocorrência e a localização, com a precisão disponível. Se a fonte
informa apenas mês e ano, o evento pode aparecer nas consultas mensais e
anuais. A busca por um dia específico exige que o dia seja conhecido.

### Fonte (`Source`)

Quem publica a informação, como uma prefeitura, um órgão de Defesa Civil
ou um veículo de imprensa. Uma fonte pode publicar várias evidências.

### Evidência (`Evidence`)

Publicação ou registro que sustenta uma ocorrência. Guarda a fonte, a URL
original e a data de publicação, quando conhecida. A data de publicação é
independente da data do evento. Uma ocorrência pode reunir várias evidências,
como um boletim da prefeitura e uma reportagem sobre o mesmo alagamento.

## Consequências

Os vínculos das ocorrências usam o identificador interno da localidade. Para
importar dados de outro país, configuramos o mapeamento de suas localidades
e identificadores externos. Nomes iguais podem ocorrer em localidades
diferentes. O nome serve para exibição e busca, e o identificador interno
serve para estabelecer vínculos.
