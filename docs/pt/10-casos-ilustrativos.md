# 🔍 10 · Casos Ilustrativos

*Como as regras aparecem em incidentes reais, contados de forma genérica*

> [!NOTE]
> Os casos abaixo são destilados de incidentes medidos no ecossistema de origem da EEE. Nomes de serviços, flags e números exatos foram removidos de propósito: o que importa é a **forma** do defeito e a regra que o pega. Qualquer plataforma multi-tenant com agentes reproduz essas formas.

---

## Caso 1 · Três flips corretos e doze dias de silêncio

**Forma:** composição não exercitada.

**O que aconteceu.** Em uma mesma janela de deploy, três gates de segurança viraram de `shadow` para `enforce`: trava de escrita na cadeia de auditoria, exigência de token no serviço de inferência e admissão estrita no serviço de autorização. Cada flip tinha pré-voo próprio, testes verdes e autor responsável. Um job em lote horário, que consultava o serviço de autorização para descobrir **quem era administrador** da conta, não enviava cabeçalho de credencial. Com a admissão estrita, passou a receber `403`. O orquestrador marcou cada execução como `dead`, e **nenhum alerta soou**: o gate quebrou a **pergunta**, não a resposta. O volume diário de tarefas caiu a zero por doze dias.

**O que pegou.** Uma leitura de série temporal com o processo gerador nomeado (R4): o job é horário, o silêncio era contínuo, não periódico.

**Regras.**
- Pré-voo ganha o item **composição**: quais outros gates viraram nesta janela, e o **produto** foi exercitado com comando e resultado.
- Reversão ensaiada: a flag voltou a `shadow` em um commit; o ledger foi atualizado no mesmo commit.
- A credencial do job em lote foi provisionada **antes** do novo flip (precondição de estado), com o comando de verificação registrado.

## Caso 2 · O sumidouro de auditoria que apagava a prova

**Forma:** fail-closed onde devia ser fail-open durável (R7).

**O que aconteceu.** Um endpoint de gravação de auditoria passou a devolver `422` por um defeito de ordem de decoradores: a função errada ficou vinculada à rota. A tarefa que gerou o evento **prosseguiu**; o registro do que aconteceu no mundo **não foi gravado**. Centenas de eventos se perderam em uma janela de horas, sem erro visível no caminho principal.

**O que pegou.** Um par discordável (R2): contagem de eventos emitidos pelo produtor *versus* contagem de registros gravados pelo sumidouro.

**Regras.**
- Decisão de acesso falha **fechando**; sumidouro de evidência falha **aberto com buffer durável**: a mensagem vai para uma fila persistente e nunca é descartada.
- A matriz M11 ganhou a metade que faltava: modos de falha de **sumidouros**, não só de gates.
- Controle negativo: um teste com payload corrompido prova que o alerta dispara **sem** abortar a cadeia de custódia.

## Caso 3 · O chamador que se declarava interno

**Forma:** resposta plausível (instância clássica) e evidência de existência sem alcance (R3).

**O que aconteceu.** O orquestrador lia o tipo do chamador **do corpo da requisição**. Um cliente externo que enviasse `"caller_type": "internal"` pulava o classificador de risco e as quotas do tenant. O gate funcionava perfeitamente: validava permissões sobre um sujeito **fornecido pelo atacante**.

**O que pegou.** Um reality-check com a sonda adversarial: a mesma requisição forjada passou de `500` com gate pulado para `403` bloqueado pelo classificador depois do arco.

**Regras.**
- Identidade é derivada **do token assinado a cada salto**, nunca do payload. Campos de identidade no corpo são rejeitados (`422`).
- O arco seguiu `off → shadow → enforce` com flag explícita e ledger; a matriz viva de casos (interno legítimo, interno declarado sem prova, externo) virou tabela de decisão testada.
- Critério de saída em forma de **aresta**: "nenhuma execução alcança dado de tenant além do seu acesso autorizado, verificado de dentro do cluster".

## Caso 4 · O stub que virou produção

**Forma:** fallback silencioso para stub; mock que vira medida.

**O que aconteceu.** Quando o transporte para o serviço a jusante falhava, um caminho de stub assumia e devolvia `status=success` com um texto de resposta, uma contagem de tokens fixa e uma referência de auditoria sintética. O chamador nunca viu a falha. Em outro ponto do mesmo sistema, um andaime gravava um score de qualidade constante em milhares de registros, lidos a jusante como medição viva.

**O que pegou.** Em ambos, um par discordável: contagem de valores **distintos** *versus* contagem de registros (milhares de linhas, **um** valor distinto).

**Regras.**
- O stub foi colocado atrás de uma flag com default `off`, valor explícito e log alto no boot. Falha de transporte devolve `503` sem `answer`.
- **Raio histórico medido** antes do conserto: nenhuma tarefa real havia consumido o stub (zero sentinelas em centenas de tarefas). O número entrou no fechamento.
- Proveniência por atributo: `real | curated | unknown`; o andaime deixou de injetar valores.
- Gatilho de aposentadoria verificável: a flag só sai quando a busca por referências nos testes retorna vazio.

## Caso 5 · A flag que não fazia nada

**Forma:** flag fantasma e caminho `enforce` inexistente (R26).

**O que aconteceu.** Uma ADR planejava a fase "flip para enforce" de um modo de autenticação de leitura. Ao briefar a fase, descobriu-se que o módulo só emitia um *warning*: o caminho de negação **não existia**. Em outro serviço, uma flag de autenticação estava declarada na configuração com **zero consumidores** no código.

**O que pegou.** Uma asserção **sintática** sobre o mecanismo (R8): busca no AST por consumidores da flag e pelo ramo de negação, antes de escrever o item de brief.

**Regras.**
- Nomear a fase na ADR não a constrói: verificar o mecanismo antes de briefar.
- Sweep da Fase 8 lista flags declaradas sem consumidor; cada uma é removida ou ganha consumidor.

## Caso 6 · A dívida que anunciou a própria quitação

**Forma:** registro de dívida como detector de fechamento (R29b).

**O que aconteceu.** Uma asserção negativa (*"a mutação de política **não** exige credencial"*) estava registrada como dívida em `xfail(strict=True)`. Quando a admissão foi implementada em outro arco, o teste passou a `XPASS` e **falhou a suíte**: o registro de dívida denunciou que a dívida tinha sido quitada, sem que ninguém tivesse desenhado isso.

**Regra.** Dívida negativa registra-se sempre `strict`: é o `strict` que faz o registro trabalhar nos dois sentidos. Em um arco em que os instrumentos de medição mentiram cinco vezes, foi o único que anunciou boa notícia que ninguém pediu.

## O que os seis casos têm em comum

| Caso | O valor parecia... | ...mas era |
|---|---|---|
| 1 | Três gates corretos | Um produto não exercitado |
| 2 | Requisição rejeitada corretamente | Prova de evento destruída |
| 3 | Gate validando permissão | Sujeito forjado pelo chamador |
| 4 | Sucesso com telemetria | Stub respondendo por falha de transporte |
| 5 | Controle configurável | Flag sem consumidor |
| 6 | Teste "falhando como esperado" | Propriedade já verdadeira |

Em todos, **o par de valores denunciou**, nunca o valor isolado. É a razão de a R2 ser a regra central do refinamento empírico.
