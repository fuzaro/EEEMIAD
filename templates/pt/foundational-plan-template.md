# 🎯 PLAN FUNDACIONAL · [Projeto]

*Camada 1 da hierarquia da verdade (EEEMIAD ch. 03; ch. 08 §1 passo 2). **Uma página.** Toda ADR cita uma seção deste arquivo em `justified_by`. Escrito a partir do [pedido](pedido.md); quem decide aprova (`done@gate`).*

```yaml
status: rascunho   # rascunho → aprovado (data e quem aprovou)
aprovado_por:
aprovado_em:
```

## §1 Por que o sistema existe

[Uma ou duas frases: que problema resolve e para quem. Sem tecnologia.]

## §2 O que o sistema não pode fazer

[Lista curta de proibições, cada uma verificável. Ex.: "aceitar registro sem os campos obrigatórios"; "expor dado pessoal em log"; "perder um número já emitido".]

- 

## §3 Invariantes

[Propriedades que valem sempre, em qualquer versão. Ex.: "número único por ano"; "todo registro tem dono".]

- 

## §4 Posturas de falha padrão

| Tipo de operação | Postura | Significado |
|---|---|---|
| Decisão (autorizar, validar, aceitar) | **fail-closed** | na dúvida ou em falha de dependência, nega |
| Evidência (log, auditoria, métrica) | **fail-open durável** | a operação segue; o registro vai para um buffer que não se perde |

## §5 Orçamentos

[Metas medíveis: tempo de resposta (ex.: p95 < 300 ms), volume, disponibilidade, custo. Sem número, não é orçamento.]

## §6 Fora de escopo

[O que esta versão não faz, com a data da decisão. Cada item aparece como **excluído** na matriz pedido × arco.]

## §7 Insumos

[Que insumos existem (layout de banco, telas, template de UX…), onde estão e com que nível de prova (R15). Um documento é **nível 1**: material de entrada, não verdade. Contradição entre insumo e pedido vai para a fase de perguntas.]
