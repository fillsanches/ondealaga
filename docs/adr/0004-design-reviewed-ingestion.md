# ADR 0004 - Projetar a coleta automatizada com revisão editorial

## Status

Proposto para o M6.

## Contexto

O Onde Alaga precisa coletar evidências de fontes externas, extrair dados
com rastreabilidade e encaminhá-los à mesma revisão editorial usada nas
outras entradas. A base para ocorrências e cobertura está no ADR 0002. A
divisão de responsabilidades segue o ADR 0003.

## Proposta

| Camada | Responsabilidade |
| --- | --- |
| Interface | Painel para configurar fontes e horários, disparar coletas, acompanhar execuções e revisar candidatos. |
| Aplicação | Coordenar descoberta, coleta, extração e revisão. Controlar permissões, execuções, retentativas, cancelamento e a transação de publicação. Definir os contratos usados pelos conectores e provedores de IA. |
| Domínio | Aplicar regras de proveniência, precisão de data e local, cobertura e publicação. Indicar possíveis duplicidades para a revisão com base em local, data, tipo e evidência. |
| Infraestrutura | Adaptar cliente HTTP, serviço de busca, coleta autorizada de páginas, provedor de IA, agendador, executor, armazenamento e PostGIS. |

### Execução e agendamento

Começar com execução manual registrada no banco e processada em segundo
plano por um executor separado do servidor HTTP. Usar o mesmo caso de uso
para disparos manuais e agendados. Persistir horários de execução, estado e
uma chave única por disparo agendado para impedir duplicatas em retentativas.
Um agendador simples, como cron ou um serviço gerenciado, pode disparar
execuções vencidas. Avaliar fila com RabbitMQ quando o volume, a concorrência
ou a distribuição de tarefas justificarem o custo operacional. O agendador
continua responsável por decidir quando disparar cada execução.

### Fontes e processamento

Usar conectores com limites de tempo, volume e frequência. Tratar URLs
cadastradas e vindas da busca como entradas externas: aceitar apenas
destinos públicos autorizados, validar redirecionamentos e bloquear acesso
à rede interna. Manter credenciais por fonte em gerenciamento de segredos
e fora de URLs, logs e contexto enviado ao modelo. Respeitar permissões de
acesso e restrições de coleta das fontes.

Guardar metadados da coleta no banco e, quando necessário, manter o bruto
em armazenamento privado com prazo de retenção. Registrar fonte, URL,
data de coleta e impressão digital do conteúdo. Preservar o trecho que
sustenta a decisão editorial conforme a política de retenção da fonte.

Usar Gemini como primeiro adaptador, com modelo selecionável por custo e
limites de consumo por execução. A aplicação usa o mesmo contrato de
extração para permitir adaptadores de OpenAI, xAI e outros provedores.
O extrator recebe conteúdo coletado como dado, com instruções versionadas,
exemplos e um esquema de saída. Sem acesso a credenciais ou à publicação,
devolve candidatos e os trechos que os sustentam. Validar a saída em código
antes de encaminhar à revisão. Registrar provedor, modelo e versão das
instruções para reproduzir a análise.

Começar com instruções e exemplos curados. Avaliar RAG se a extração
precisar recuperar contexto interno relevante, como glossário, regras
editoriais ou referências de localidades, e se a avaliação demonstrar
ganho na qualidade dos candidatos. As regras obrigatórias seguem no código.

### Revisão e publicação

Manter candidatos e resultados de execução em área privada de revisão.
Reprocessar uma coleta ou repetir uma aprovação deve preservar a identidade
dos itens já processados. Registrar a decisão editorial e a alteração da
ocorrência na mesma transação. Usar a evidência, o local, a data e o tipo
para sugerir vínculos com ocorrências existentes, inclusive quando uma
fonte diferente descrever o mesmo evento.

## Consequências

A automação pode ser entregue com uma fonte e um provedor. A adoção de
outros conectores, uma fila distribuída e RAG será decidida a partir do
uso e dos resultados observados.
