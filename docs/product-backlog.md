# Backlog de produto

## Consulta de ocorrências e histórico no mapa

Na home, tentar identificar a cidade. Se houver apenas o estado, abrir o
mapa da capital. Se nenhum dos dois estiver disponível, abrir o mapa do
Brasil. Manter a busca manual por cidade disponível em todos os níveis.

- **Brasil:** exibir o total de ocorrências registradas por estado.
- **Estado:** exibir o total por cidade.
- **Cidade:** exibir totais por área ou agrupamento de pontos. Ao aproximar,
  mostrar as ocorrências com data, evidências e precisão geográfica.
  Registros sem posição detalhada entram no total e ficam acessíveis em lista.

Abrir no ano atual e manter o filtro de ano ou mês ao mudar de nível. Contar
ocorrências verificadas pela data do evento, uma vez por ocorrência, mesmo
quando sustentadas por várias fontes ou relatos. Se só o ano for conhecido,
contar no ano e informar que o mês é desconhecido.

Exibir a cobertura conhecida das fontes no período. Distinguir entre
período sem cobertura conhecida, período parcialmente coberto e período
coberto sem ocorrências encontradas nas fontes consultadas. Exibir a data
de referência quando a consulta do período corrente usar apenas os dias
já transcorridos.

Oferecer uma camada de áreas com histórico, com a última ocorrência
registrada. Uma ocorrência continua disponível nessa camada nos anos
seguintes e entra apenas no total do período em que ocorreu. Relatos sobre
obras ou mudanças de condição podem gerar uma atualização datada e com
fonte após revisão, preservando o evento original.

Exibir mapas técnicos de perigo ou risco em camada própria, quando
disponíveis, com órgão, data e legenda. Exibir probabilidades somente quando
houver estudo aplicável ao local e ao fenômeno, com cenário, período e fonte.

**Entrega:** registrar cobertura no M1 e aplicar essas regras de navegação
e exibição no M3.

## Relatos de alagamento enviados pela comunidade

Permitir o envio manual por usuários, com cidade, data na precisão conhecida,
descrição e alcance informado. Aceitar número de endereço, trecho da rua, rua
com trecho desconhecido ou rua inteira explicitamente indicada. Mostrar a
precisão disponível e exigir revisão antes de representar toda a extensão
de uma rua como atingida. Conservar a referência textual se a posição
espacial ainda não puder ser validada.

Aceitar fotos, vídeos, boletins e links como evidência opcional. Remover
metadados dos arquivos publicados e permitir ocultar rostos e placas.
Após triagem, apresentar na camada comunitária os apontamentos sem
comprovação, os relatos com evidência aguardando análise e os casos em
revisão. Exibir ocorrências verificadas após decisão editorial registrada.
Se vários relatos descreverem o mesmo evento, vincular as contribuições a
uma única ocorrência e preservar as evidências e a autoria de cada relato.

**Entrega:** aproveitar a revisão editorial do M2. Iniciar a colaboração
no M7 com formulário, evidências, triagem e publicação.

## Confirmações, contestações e reputação

Permitir confirmar ou contestar um relato, com um voto editável por conta
e por relato. Pedir motivo para contestar e aceitar comentários ou novas
evidências. Uma contestação fundamentada pode reabrir a revisão. Registrar
as decisões editoriais e os motivos para que possam ser consultados.

Usar a pontuação interna para priorizar a revisão. Dar prioridade a
evidências que sustentem local e data e a confirmações independentes.
Tratar anexos repetidos como uma única evidência e dar peso limitado à
reputação do autor. A reputação cresce com contribuições avaliadas como
úteis, como correções, evidências e identificação de duplicidades. Um
usuário novo pode ter seu relato verificado se houver evidência suficiente.
Exibir os motivos da verificação, mantendo a decisão editorial como
requisito para incluir uma ocorrência nos totais históricos.

**Entrega:** adicionar votos, comentários e reputação no M7 depois de
validar o fluxo básico de envio. Usar o M8 para ampliar o fluxo de denúncia
de erros e acompanhamento das correções.

## Coleta de dados de alagamento com revisão humana

Permitir que um operador autorizado execute uma coleta na hora, agende uma
execução única ou configure uma recorrência. Cada configuração guarda fuso
horário, conjunto de cidades, fontes, período pesquisado e modo de
processamento. O operador pode pausar um agendamento recorrente.

O operador escolhe fontes do catálogo do Onde Alaga ou cadastra referências
próprias para as quais tem permissão de acesso. A coleta pode usar API
pública, API com autenticação ou leitura automatizada de páginas autorizadas.
Para descobrir fontes, o operador pode configurar uma consulta como
`onde alaga em {cidade}`. Cada localidade cadastrada gera uma consulta com
nome, divisão administrativa e país quando necessário para desambiguação.
Os resultados da busca passam pelo mesmo controle de fontes antes da coleta.

Oferecer dois modos: guardar o resultado bruto temporariamente para inspeção
ou encaminhá-lo ao provedor de IA selecionado. No modo com IA, preservar a
referência ao material original para revisão. A extração propõe ocorrências
com localidade, tipo, data e precisão geográfica conhecidas, acompanhadas de
URL e trecho de evidência. Campos desconhecidos ficam vazios. Propor cobertura
somente quando a referência documentar o intervalo consultado.

Exibir o andamento e o resultado da execução: horário, etapa, fontes
processadas, candidatos, falhas por fonte e consumo estimado de IA quando
disponível. Permitir reprocessar uma etapa com o bruto ainda disponível e
interromper o trabalho pendente, preservando os resultados já concluídos.

Na revisão, mostrar a proposta ao lado da evidência. O revisor autorizado
pode corrigir, rejeitar, vincular a uma ocorrência existente ou aprovar
individualmente ou em lote. A aprovação em lote mostra o conjunto selecionado,
valida cada item e informa os aprovados e os que exigem revisão. Registrar
quem decidiu, quando, a origem do material e o motivo da decisão. Apenas a
aprovação editorial pode inserir ou atualizar ocorrências públicas.

**Entrega:** no M6, começar com uma fonte estruturada, execução manual,
extração com Gemini e a revisão editorial do M2. Depois, adicionar
agendamentos, outros conectores e revisão em lote. Avaliar RAG no M11 a
partir das falhas observadas na extração. A [proposta de arquitetura da
coleta](adr/0004-design-reviewed-ingestion.md) detalha as responsabilidades.

## Banners para financiar a operação

Reservar espaços no layout para banners publicitários. A receita desses
espaços deve ajudar a cobrir os custos de hospedagem e operação do Onde
Alaga. A publicidade deve ser identificável e preservar o acesso à busca,
ao mapa e às fontes, inclusive no celular.

Os anúncios serão exibidos por cidade. A seleção usa a localidade da
página consultada: um anúncio de Maricá aparece na página de Maricá,
independentemente de onde a pessoa estiver.

**Retomar:** no M3, ao desenhar o frontend, para definir os espaços. A
veiculação pode entrar depois da beta pública, no M5 ou em etapa posterior.

## Nuvem de cidades mais visitadas

Exibir uma visualização no estilo nuvem de tags. O tamanho de cada nome
representa o total de visitas à página da cidade no período exibido. Cada
nome leva à página correspondente. Uma lista com os mesmos totais permite
consultar os valores e usar a visualização sem depender do tamanho do texto.

**Retomar:** depois que a medição de visitas estiver funcionando e houver
dados suficientes para comparar as páginas das cidades.

## Estatísticas públicas de visitação

Disponibilizar uma página com números agregados de visitação do portal e
por página de cidade. Exibir o período, a data de atualização e como a
métrica é calculada. A contagem é atribuída à página consultada, de modo
que uma visita à página de Maricá conte para Maricá, independentemente da
localização da pessoa. Publicar apenas totais agregados.

**Retomar:** após o M5, quando pudermos validar a coleta e a qualidade dos
dados da beta. As estatísticas serão a base da nuvem de cidades.
