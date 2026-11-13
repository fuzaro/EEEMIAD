# Diretrizes de Contribuição / Contribution Guidelines

[Português](#português) · [English](#english)

---

## Português

Obrigado pelo interesse em contribuir para a **EEEMIAD** (Engenharia Empírica Evolutiva — Metodologia de IA para Desenvolvimento).

### Princípios de contribuição

1. **Evidência sobre opinião.** Toda proposta de regra, anti-padrão ou ajuste conceitual vem com evidência observada: caso de falha documentado, medição, log ou justificativa formal. Regras entram no método quando há evidência e saem quando ela falta.
2. **Hierarquia da verdade.** Mudanças metodológicas seguem `Plan → ADR → Spec → Code`. Não altere templates, exemplos ou scripts sem atualizar o capítulo que os governa.
3. **Par discordável (R2).** Todo critério de validação proposto inclui o controle que pode discordar dele.
4. **Exemplos genéricos.** Casos ilustrativos são contados pela **forma** do defeito; nomes de produtos, serviços e números internos ficam fora.
5. **Escopo.** Este repositório descreve a EEE. Propostas sobre a instanciação em dois agentes pertencem ao repositório irmão `EEEMIAD-dual`.
6. **Multilinguismo.** Contribuições em `docs/` são submetidas em Português e Inglês, ou abertas com a etiqueta `help-wanted:translation` para Francês e Espanhol.

### Como submeter

- Abra uma *issue* descrevendo o problema empírico encontrado.
- Crie um branch com prefixo semântico (`feat/`, `fix/`, `docs/`, `skill/`, `example/`).
- Rode os exemplos e o harness:
  ```bash
  pytest -q examples/evolutionary-arc/code/tests
  python3 examples/verification-harness/verify_hierarchy.py --project-root ./examples/reference-implementation
  ```
- Abra o *pull request* com o checklist preenchido; se a mudança toca algo irreversível, inclua o bloco de pré-voo.

---

## English

Thank you for your interest in contributing to **EEEMIAD** (Evolutionary Empirical Engineering — AI Methodology for Development).

### Contribution principles

1. **Evidence over assertion.** Every proposed rule, anti-pattern or conceptual change comes with observed evidence: documented failure case, measurement, log or formal argument. Rules enter the method when evidence exists and leave when it is missing.
2. **Hierarchy of truth.** Methodological changes follow `Plan → ADR → Spec → Code`. Do not alter templates, examples or scripts without updating the chapter that governs them.
3. **Disagreeable pair (R2).** Every proposed validation criterion includes the control that can disagree with it.
4. **Generic examples.** Illustrative cases are told by the **form** of the defect; product names, service names and internal numbers stay out.
5. **Scope.** This repository describes EEE itself. Proposals about the two-agent instantiation belong to the sibling repository `EEEMIAD-dual`.
6. **Multilingual.** Contributions to `docs/` are submitted in Portuguese and English, or opened with the `help-wanted:translation` label for French and Spanish.

### How to submit

- Open an issue describing the empirical problem.
- Create a branch with a semantic prefix (`feat/`, `fix/`, `docs/`, `skill/`, `example/`).
- Run the examples and the harness:
  ```bash
  pytest -q examples/evolutionary-arc/code/tests
  python3 examples/verification-harness/verify_hierarchy.py --project-root ./examples/reference-implementation
  ```
- Open the pull request with the checklist filled; if the change touches anything irreversible, include the pre-flight block.
