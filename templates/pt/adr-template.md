# ADR-[XXX]: [Título Curto e Imperativo da Decisão]

```yaml
status: PROPOSED # [PROPOSED | ACCEPTED | REJECTED | DEPRECATED | SUPERSEDED]
date: YYYY-MM-DD
deciders: [Agente Reflexivo (Cowork), Operador Humano]
hierarchy_layer: ADR
governs: [specs/servico-alvo.md]
justified_by: [Plan/docs/framework-principles.md §Princípio X]
replaces: [] # Ex: [ADR-012]
eee_phase: 2 # Fase 2 (Contratos) ou Fase 6 (Abstração)
```

---

## 1. Contexto do Problema e Evidência Empírica
> *Qual o problema concreto observado em runtime ou na especificação?*
> *Qual o impacto medido ou o risco de segurança/integridade?*

- **Origem Empírica:** [Citar achado, teste vermelho ou incidente real com commit/data].
- **Sintoma Observado:** [Descrição precisa da falha ou lacuna].
- **Princípios Afetados:** [Princípios do Plan impactados].

---

## 2. Decisão Arquitetural
> *Qual escolha técnica estamos fazendo formalmente?*

- **D1 ([Título da Sub-decisão]):** [Descrição imperativa da regra adotada].
- **D2 ([Título da Sub-decisão]):** [Descrição imperativa da regra adotada].
- **D3 ([Postura em Falha M11]):** [Definição explícita de Fail-Closed vs Fail-Open com Log Durável].

---

## 3. Alternativas Consideradas

| Alternativa | Prós | Contras | Veredito |
|---|---|---|:---:|
| **Opção A:** [Descrição] | • [Vantagem] | • [Desvantagem] | **REJEITADA** |
| **Opção B (Escolhida):** [Descrição] | • [Vantagem] | • [Desvantagem] | **ACEITA** |
| **Opção C:** [Descrição] | • [Vantagem] | • [Desvantagem] | **REJEITADA** |

---

## 4. Consequências Assumidas

### Positivas
- [O que ganhamos em segurança, integridade ou desacoplamento].

### Negativas / Custos Aceitos
- [Complexidade adicional, overhead de rede, latência ou esforço de migração].

---

## 5. Superfície Contratual Introduzida (§7)
- **Invariantes Novas:** [Regras estritas que nunca podem ser violadas].
- **Controle de Acesso:** [Políticas RBAC / FGA necessárias].
- **Auditoria Obrigatória:** [Eventos de auditoria gerados].

---

## 6. Precondições e Pré-Voo de Implementação
- **Precondição de Estado:** [Tuplas, tabelas ou variáveis que precisam existir antes do código].
- **Comando de Verificação:** `[comando]`
