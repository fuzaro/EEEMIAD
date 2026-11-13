# 📐 ADR-[XXX] · [Título curto e imperativo da decisão]

```yaml
status: PROPOSED # PROPOSED | ACCEPTED | REJECTED | DEPRECATED | SUPERSEDED
date: YYYY-MM-DD
deciders: [papel que decide, operador humano]
hierarchy_layer: ADR
governs: [specs/componente.md]
justified_by: [Plan/docs/principios.md §Princípio X]
replaces: [] # ex.: [ADR-012]
eee_phase: 2 # 2 (contrato) | 6 (abstração após repetição)
ratified_by: null # artefato separado que cita evidência, SHA e nível R15 — quem propõe não ratifica
```

---

## 1. Contexto e evidência empírica

- **Origem empírica:** [achado, teste vermelho ou incidente, com data e referência].
- **Sintoma observado:** [descrição precisa da falha ou lacuna; nível de ground truth R15].
- **Princípios afetados:** [princípios do Plan impactados].

## 2. Decisão

- **D1 · [título]:** [regra imperativa].
- **D2 · [título]:** [regra imperativa].
- **D3 · Postura de falha (M11):** [fail-closed para decisão; fail-open com buffer durável para evidência].
- **D4 · Flag e fases:** [`FLAG_X ∈ {off, shadow, enforce}`, default `off`; gate de saída de cada fase].

## 3. Alternativas consideradas (≥ 2)

| Alternativa | Prós | Contras | Veredito |
|---|---|---|:---:|
| **A ·** [descrição] | [vantagem] | [desvantagem] | **REJEITADA** |
| **B (escolhida) ·** [descrição] | [vantagem] | [desvantagem] | **ACEITA** |
| **C ·** [descrição] | [vantagem] | [desvantagem] | **REJEITADA** |

## 4. Consequências assumidas

- **Positivas:** [o que se ganha em segurança, integridade, desacoplamento].
- **Negativas / custos aceitos:** [complexidade, latência, esforço de migração].

## 5. Superfície contratual introduzida (contratos explícitos)

- **Invariantes novas:** [regras que nunca podem ser violadas].
- **Controle de acesso:** [políticas exigidas].
- **Auditoria obrigatória:** [eventos gerados].
- **Spec a atualizar no mesmo arco (R30):** [tabelas, flags, jobs criados por esta decisão].

## 6. Precondições e varredura de dependentes

- **Precondição de estado:** [tuplas, tabelas, variáveis que precisam existir antes do código]. Comando de verificação: `[comando]`.
- **Decisões que se apoiavam na premissa alterada (R9):** [lista a revisar].
