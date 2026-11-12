# EEEMIAD — Documentation en Français
## Ingénierie Empirique Évolutive — Méthodologie d'Intelligence Artificielle pour le Développement

> **État:** Échafaudage initial & feuille de route de traduction.  
> Pour la documentation complète et opérationnelle, veuillez consulter les versions en [Português](../pt/01-visao-geral.md) ou en [English](../en/01-overview.md).

---

### Résumé Exécutif
L'**EEEMIAD** est un cadre d'ingénierie logicielle formel conçu pour éliminer les défaillances critiques des systèmes développés par des agents autonomes et des modèles de langage (LLMs) :
1. **La Hiérarchie de Vérité (§2):** `Plan → ADR → Spec → Code`. Le code ne gagne jamais contre la spécification.
2. **La Pile de DONE Stratifiée:** Interdiction du "done" sans qualificatif (`done@structural`, `done@functional`, `done@gate`, `done@purpose`).
3. **Le Workflow Dual-Agent:** Séparation stricte entre l'agent réflexif (conception et ADRs) et l'agent exécutif (implémentation et reality-check).
4. **Les 10 Règles Empiriques:** Protection contre la "famille des réponses plausibles".

---

### Feuille de Route de Traduction (Roadmap)
- [ ] `00-manifeste.md` — Le manifeste de l'attention humaine finie
- [ ] `01-vue-d-ensemble.md` — Présentation générale et ontologie
- [ ] `02-principes.md` — Les 8 principes fondamentaux
- [ ] `03-hierarchie-de-la-verite.md` — La cascade Plan-ADR-Spec-Code
- [ ] `04-phases-du-cycle.md` — Les 8 phases du cycle de vie
- [ ] `05-regles-de-raffinement.md` — Les 10 règles opérationnelles
- [ ] `06-workflow-dual-agent.md` — Conception vs Exécution
- [ ] `07-anti-patrons.md` — Catalogue des pièges architecturaux
- [ ] `08-guide-d-application.md` — Guide pas à pas (Greenfield & Brownfield)
- [ ] `09-fondements-academiques.md` — Théorie des graphes et méthodes formelles
- [ ] `10-etudes-de-cas.md` — Cas réels et incidents résolus
