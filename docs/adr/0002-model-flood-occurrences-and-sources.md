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
O banco guarda ano, mês e dia em campos próprios e mantém os componentes
desconhecidos vazios. A localização pode ser um ponto ou uma área, com
precisão exata ou aproximada. Quando só houver uma referência descritiva,
como o nome de um bairro, podemos guardá-la sem atribuir coordenadas.

### Fonte (`Source`)

Quem publica a informação, como uma prefeitura, um órgão de Defesa Civil
ou um veículo de imprensa. Uma fonte pode publicar várias evidências.

### Evidência (`Evidence`)

Publicação ou registro que sustenta uma ocorrência. Guarda a fonte, a URL
original e a data de publicação, quando conhecida. A data de publicação é
independente da data do evento. Uma ocorrência pode reunir várias evidências,
como um boletim da prefeitura e uma reportagem sobre o mesmo alagamento.
A mesma fonte e URL identificam uma única evidência para cada ocorrência.
Uma publicação pode ser vinculada a mais de uma ocorrência.

### Cobertura da fonte (`SourceCoverage`)

Intervalo de dias, com início e fim inclusivos, que uma referência documenta
para uma fonte e uma localidade. Registrar a referência mesmo quando ela
informa zero ocorrências. Permitir vários intervalos por fonte e localidade,
inclusive sobrepostos ou descontínuos. A cobertura vem do alcance declarado
na referência. Relatos pontuais, por si sós, documentam ocorrências.

Para classificar a cobertura de uma consulta, considerar a união dos
intervalos das fontes relevantes para aquela localidade, limitada às datas
consultadas. Classificar como total se todos os dias forem cobertos, parcial
se houver dias cobertos e lacunas, e desconhecida se não houver interseção
com os intervalos conhecidos. Cobertura descreve as fontes disponíveis.
Um resultado vazio se refere às ocorrências encontradas nessas fontes.

### Proposta de ocorrência (`OccurrenceProposal`)

As propostas editoriais ficam em `occurrence_proposals`, com evidências
opcionais em `proposal_evidence`. A proposta começa como pendente e
preserva a mesma precisão de data prevista para a ocorrência. O cadastro da
proposta e das evidências usa uma única transação. As ocorrências públicas
continuam em `occurrences`.

## Consequências

Os vínculos das ocorrências usam o identificador interno da localidade. Para
importar dados de outro país, configuramos o mapeamento de suas localidades
e identificadores externos. Nomes iguais podem ocorrer em localidades
diferentes. O nome serve para exibição e busca, e o identificador interno
serve para estabelecer vínculos.
