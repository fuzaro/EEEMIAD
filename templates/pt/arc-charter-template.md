# 📜 CHARTER · [Nome do Arco]

*Contrato de abertura de um arco EEE: propriedade, refutação, flag, posturas e gate de saída*

```yaml
arc_id: ARC-[XXX]
governing_adr: ADR-[XXX] (status=ACCEPTED)
target_spec: specs/[componente].md
flag: [NOME_DA_FLAG]
flag_domain: [off | shadow | enforce]
flag_default_in_code: off
delegation: none # none | tiered: só com resposta positiva do operador na fase de perguntas (08 §6)
request_item: [item da matriz pedido × arco que este arco atende, nas palavras do pedido (08 §1 passo 2)]
opened: YYYY-MM-DD
owner: [papel ou pessoa que decide]
```

---

## 1. Propriedade alvo (R11: propriedade, não mecanismo)

> *"[Enunciado da propriedade em uma frase verificável. Ex.: nenhuma leitura de recurso de tenant é servida sem credencial válida.]"*

## 2. Condição de refutação

> *"[Observação concreta que, se ocorrer, refuta o arco. Ex.: uma requisição sem bearer que receba 200.]"*

Sem este item o arco não abre.

## 3. Postura de falha (linha M11)

| Operação | Condição de erro | Postura | Resposta observável |
|---|---|---|---|
| `[op]` | dependência indisponível | **Fail-closed** (decisão) ou **Fail-open com buffer durável** (evidência) | `[503 / buffer + log alto]` |

## 4. Fases e gates

| Fase | Entrega | Gate para avançar |
|---|---|---|
| **P1 · Fatia fina (flag off)** | Mecanismo completo, comportamento neutro, stubs marcados | Bateria (1)(2)(3) verde; dívidas em `xfail(strict)`; ledger e spec atualizados |
| **P2 · Shadow** | Intent-log com par discordável; detecção de divergência; critério de saída consultável | 0 refutações em ≥ **N = [__]** oportunidades reais; processo gerador nomeado |
| **P3 · Hardening** | Desmock por colaborador; uma linha M11 por modo de falha, cada uma com teste de injeção | Raio histórico do stub medido; gatilho de aposentadoria verificável |
| **P4 · Cut-over** | Pré-voo completo; flip e ledger no mesmo commit | Reprodução ao vivo da propriedade **e** da refutação (nível 4) |

## 5. Pré-voo do cut-over (preencher antes do flip)

```
1. Efeitos colaterais além do alvo:          ______
2. Reversível? [SIM/NÃO] (se NÃO → STOP):     ______
3. Rollback ensaiado (comando + tempo):       ______
4. Precondição de estado (comando + saída):   ______
5. Composição: outros gates nesta janela?     ______
   Produto exercitado? (comando + resultado): ______
6. Mecanismo enforce existe? (asserção AST):  ______
```

## 6. Janela de observação e aposentadoria

- Janela pós-enforce antes de remover a flag: `[__ oportunidades | __ semanas]`
- Comando que prova zero consumidores da flag: `grep -rl [FLAG] src/ tests/` → vazio

## 7. Fechamento

```yaml
closed: YYYY-MM-DD
deficit_query: "[consulta/teste que detectou o déficit]"
deficit_result: 0
done_tier: done@funcional
ground_truth_level: 4
```
