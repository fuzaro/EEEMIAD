# Diretrizes de Contribuição / Contribution Guidelines

[Português](#português) | [English](#english)

---

## Português

Agradecemos o seu interesse em contribuir para a **EEEMIAD** (Engenharia Empírica Evolutiva - Metodologia de Inteligência Artificial para Desenvolvimento). 

### Nossos Princípios de Contribuição
1. **Evidência sobre Opinião:** Qualquer proposta de adição conceitual ou novo anti-padrão deve ser acompanhada de evidência observada (caso de falha documentado, logs, métricas empíricas ou justificativa formal).
2. **Hierarquia da Verdade:** Mudanças metodológicas seguem o fluxo `Plan → ADR → Spec → Code`. Não altere templates ou scripts sem atualizar as especificações e decisões correspondentes.
3. **Pares Discordáveis:** Todo critério de validação sugerido deve incluir um par que possa discordar (Regra R2).
4. **Multilinguismo:** As contribuições nos núcleos normativos (`docs/`) devem ser submetidas em Português e Inglês, ou abertas com tag `help-wanted:translation` para Francês e Espanhol.

### Como Submeter
- Abra uma Issue detalhando o problema empírico encontrado.
- Crie um branch com prefixo semântico (`feat/`, `fix/`, `docs/`, `skill/`).
- Execute o harness de validação: `python3 examples/verification-harness/verify_hierarchy.py`.
- Abra o Pull Request com checklist de pré-voo preenchido.

---

## English

Thank you for your interest in contributing to **EEEMIAD** (Evolutionary Empirical Engineering - AI Methodology for Development).

### Contribution Principles
1. **Evidence over Assertion:** Any proposed conceptual addition or anti-pattern must be backed by observed empirical evidence (documented failure case, logs, metrics, or formal proof).
2. **Hierarchy of Truth:** Methodological evolution adheres to `Plan → ADR → Spec → Code`. Do not alter templates or test scripts without updating corresponding specifications and decisions.
3. **Disagreeable Pairs:** Every proposed validation criterion must carry a counter-balancing pair (Rule R2).
4. **Multilingual Consistency:** Core normative contributions in `docs/` should be provided in both Portuguese and English, or tagged with `help-wanted:translation` for French and Spanish tracks.

### Submission Process
- Open an Issue detailing the observed empirical defect or requirement.
- Create a feature branch using semantic prefixes (`feat/`, `fix/`, `docs/`, `skill/`).
- Run the verification harness: `python3 examples/verification-harness/verify_hierarchy.py`.
- Submit your Pull Request ensuring the blast-radius checklist is completed.
