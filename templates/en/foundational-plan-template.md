# 🎯 FOUNDATIONAL PLAN · [Project]

*Layer 1 of the hierarchy of truth (EEEMIAD ch. 03; ch. 08 §1 step 2). **One page.** Every ADR cites a section of this file in `justified_by`. Written from the [request](request.md); who decides approves it (`done@gate`).*

```yaml
status: draft   # draft → approved (date and who approved)
approved_by:
approved_on:
```

## §1 Why the system exists

[One or two sentences: which problem it solves and for whom. No technology.]

## §2 What the system must not do

[A short list of prohibitions, each verifiable. E.g. "accept a record without the mandatory fields"; "expose personal data in a log"; "lose a number already issued".]

- 

## §3 Invariants

[Properties that always hold, in any version. E.g. "one number per year"; "every record has an owner".]

- 

## §4 Default failure postures

| Kind of operation | Posture | Meaning |
|---|---|---|
| Decision (authorise, validate, accept) | **fail-closed** | when in doubt or when a dependency fails, deny |
| Evidence (log, audit, metric) | **durable fail-open** | the operation proceeds; the record goes to a buffer that is not lost |

## §5 Budgets

[Measurable targets: response time (e.g. p95 < 300 ms), volume, availability, cost. Without a number it is not a budget.]

## §6 Out of scope

[What this version does not do, with the date of the decision. Each item appears as **excluded** in the request × arc matrix.]

## §7 Inputs

[Which inputs exist (database layout, screens, UX template…), where they are and at which proof level (R15). A document is **level 1**: input material, not truth. A contradiction between an input and the request goes to the question phase.]
