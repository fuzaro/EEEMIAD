# 🧪 DIÁRIO DE EVIDÊNCIAS · [Projeto]

*Uma linha por mudança de estado relevante, no mesmo commit da mudança, sempre com comando e resultado (EEEMIAD ch. 08 §8.1)*

**Quando escrever:** arco aberto ou fechado, flip de flag, deploy, rollback, incidente, decisão do operador, achado sobre o método. **Sem comando e resultado, não há linha.**

**Achado sobre o método:** **ok** (a prescrição serviu como está) · **atrito** (serviu, mas custou mais do que devia ou exigiu interpretação) · **lacuna** (o método não cobre; houve decisão local). Atritos e lacunas recebem um código (A1, L1…) e viram propostas para o método, com esta entrada como origem.

| # | Data | Contexto | Prescrição (cap. / regra) | O que foi feito | Evidência (comando → resultado, nível R15) | Achado |
|---|---|---|---|---|---|---|
| 1 | AAAA-MM-DD | [ARC-XXX · flip · deploy · incidente] | [ex.: ch. 04 Fase 7, pré-voo] | [o que mudou, em uma ou duas frases] | [`comando` → saída resumida; link para o charter ou a evidência de cut-over; nível] | **ok** |
| 2 | AAAA-MM-DD | [ARC-XXX] | [ex.: R2] | [ ] | [ ] | **atrito A1** · [o que custou e por quê; proposta] |

<!--
Regras:
- A linha entra no commit da mudança, como o ledger de flags no flip.
- O diário não substitui o charter: o charter é a prova de um arco; o diário é o índice cronológico entre arcos.
- Não registre valor secreto nem dado privado; registre onde está e como conferir.
- Entradas não se apagam. Um erro numa entrada antiga é corrigido por uma entrada nova que a cita.
-->
