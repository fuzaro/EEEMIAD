# EEEMIAD — Documentation en Français

*Ingénierie Empirique Évolutive — Méthodologie d'Intelligence Artificielle pour le Développement*

> [!NOTE]
> **État :** échafaudage initial et feuille de route de traduction.
> Pour la documentation complète, consultez les versions en [Português](../pt/01-visao-geral.md) ou en [English](../en/01-overview.md).

---

## Résumé exécutif

L'**EEE** est une discipline d'ingénierie logicielle pour les systèmes où des modèles de langage et des agents autonomes construisent du code :

1. **Hiérarchie de la vérité :** `Plan → ADR → Spec → Code`. Le code ne gagne jamais une divergence parce qu'il est déjà déployé.
2. **Pile de DONE stratifiée :** interdiction du « done » sans qualificatif (`done@structural`, `done@functional`, `done@gate`, `done@purpose`).
3. **Construction évolutive :** fine tranche → stubs et mocks → flags `off | shadow | enforce` → tests avec paire discordante → arcs qui se ferment par mesure, jamais par déclaration.
4. **Règles du raffinement empirique :** défenses mesurées contre la « famille des réponses plausibles ».

## Feuille de route de traduction

- [ ] `00-manifeste.md` — Le manifeste de l'attention humaine finie
- [ ] `01-vue-d-ensemble.md` — Définition, les deux chemins, les trois rôles
- [ ] `02-principes.md` — La pile de DONE et les onze principes
- [ ] `03-hierarchie-de-la-verite.md` — La cascade et la réconciliation ascendante
- [ ] `04-phases-du-cycle.md` — Les huit phases
- [ ] `05-regles-du-raffinement.md` — R1–R10 et les règles de construction
- [ ] `06-construction-evolutive.md` — Stubs, mocks, flags et arcs
- [ ] `07-anti-patrons.md` — Catalogue des pièges mesurés
- [ ] `08-guide-d-application.md` — Greenfield, brownfield, checklist d'arc
- [ ] `09-fondements-academiques.md` — Bibliographie et épistémologie
- [ ] `10-cas-illustratifs.md` — Incidents racontés par leur forme
- [ ] `11-glossaire.md` — Termes
