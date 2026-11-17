# 🛠️ 08 · Practical Application Guide

*How to adopt EEE in new and legacy projects, in objective steps*

> [!NOTE]
> This chapter is deliberately operational. The rationale is in [02](02-principles.md), [05](05-refinement-rules.md) and [09](09-academic-foundation.md); here there is only what to do, in which order, and how to know it is finished.

---

## 1. New project (greenfield)

```mermaid
flowchart TD
    G1["1 · Governance tree<br/>Plan/ · Plan/decisions/ · specs/ · tests/"] --> G2["2 · Foundational Plan<br/>purpose, principles, invariants, default postures"]
    G2 --> G3["3 · ADR-001 (initial architecture)<br/>PROPOSED → debate → ACCEPTED"]
    G3 --> G4["4 · 1:1 Specs + M11<br/>schemas, routes, DDL, failure modes"]
    G4 --> G5["5 · Charter of the first arc<br/>property + refutation + flag"]
    G5 --> G6["6 · Thin slice with stubs (P1, flag OFF)<br/>red test → green → neighbour barred"]
    G6 --> G7["7 · De-mock + shadow + enforce<br/>pre-flight, fault injection, window"]
    G7 --> G8["8 · Mechanical closure<br/>harness green + deficit query = 0 → done@tier"]
```

### Step 1 · Governance tree

```bash
mkdir -p Plan/decisions Plan/docs specs tests/unit tests/integration tests/adversarial eee/state
```

| Directory | Layer | Content |
|---|---|---|
| `Plan/docs/` | 1 | Purpose, principles, invariants, limits |
| `Plan/decisions/` | 2 | Numbered ADRs ([template](../../templates/en/adr-template.md)) |
| `specs/` | 3 | Living contracts + M11 matrix ([template](../../templates/en/failure-modes-m11-template.md)) + flag ledger ([template](../../templates/en/flag-ledger-template.md)) |
| `tests/` | 4 | Suites with disagreeable pairs; `adversarial/` is written without reading the implementation |
| `AGENTS.md` | operations | Entry point for people and for agents of any harness: hard rules, reading order, commands ([template](../../templates/en/agents-entry-template.md), §8.2) |
| `eee/log.md` | operations | Evidence journal, permanent ([template](../../templates/en/evidence-journal-template.md), §8.1) |
| `eee/state/` | operations | Operational state: what is on where, pending items, operator decisions; **where** each secret lives, never its value (§8.2) |
| `tools/gate.sh` | operations | Single gate command ([example](../../examples/verification-harness/gate.sh), §8.3) |

The "operations" rows are not a fifth layer of the hierarchy: they decide nothing. They record what happened, where things are and how to verify.

### Step 2 · Foundational Plan
One page. Contains: why the system exists; what it **must not** do; default failure postures (decision → fail-closed; evidence → durable fail-open); global budgets.

Keep beside it the **original request**, in the words of whoever asked (`Plan/docs/request.md`), and a **request × arc matrix**: each item of the request points to an arc or to an explicit exclusion, with date and decider. The Plan is a reading of the request and can be wrong; the matrix is what lets you see the error.

### Step 3 · ADR-001
Born `PROPOSED`. Has ≥ 2 alternatives, consequences and numbered decisions (D1...Dn). Ratification is a separate commit citing Phase 1 evidence.

### Step 4 · Specs and M11
For each interface: input and output schema, response codes, pre- and post-conditions, and **one M11 row per failure mode**. A spec without M11 is not complete.

### Step 5 · Charter of the first arc
Use the [charter template](../../templates/en/arc-charter-template.md). Property, refutation condition, flag with domain and default, exit gate in real opportunities, observation window.

### Step 6 · Thin slice (P1)
- Flag `off` in code, explicit in the deployment.
- Stubs tagged and with provenance `unknown`.
- Minimum battery: (1) target passes, (2) legacy passes, (3) neighbour bars. Debts in `xfail(strict=True)`.
- **Before accepting the green:** inject the defect and see the red.

### Step 7 · De-mock, shadow and enforce
- De-mock one collaborator at a time, keeping the shape contract.
- `shadow`: intent log + divergence detection + exit-criterion endpoint.
- `enforce` only with a complete pre-flight ([04 · Phase 7](04-cycle-phases.md)); flip and ledger in the same commit.
- Fault injection for every M11 row (unavailable, timeout, 5xx, invalid body, empty config).

### Step 8 · Mechanical closure

```bash
python3 examples/verification-harness/verify_hierarchy.py --project-root .
python3 examples/verification-harness/check_falsification.py --test-dir ./tests
```

In the project, these commands and the other verifiers (language adapter, DDL parity, suite) sit behind **one** gate command (§8.3).

Closes when: gate green; the query that detected the deficit returns zero; the tier is declared (`done@functional`, R15 proof level). Anything above that is `done@gate` and belongs to the human.

> [!IMPORTANT]
> **Read the `examined` line, not only the verdict.** The verifier fails when it finds no code to examine; in Phase 2, before code exists, pass `--allow-missing-code`. A verifier that examines nothing must not say it passed. TypeScript/Next.js projects use the [TypeScript adapter](../../examples/verification-harness/typescript/README.md); other languages need an adapter that keeps the same contract.

## 2. Legacy project (brownfield)

Adopting EEE on existing code is reverse engineering in **four stages**, with one rule: **do not edit the living spec while the census is in progress**.

```mermaid
sequenceDiagram
    autonumber
    participant Legacy as Live code
    participant AST as AST census
    participant Matrix as Divergence matrix
    participant New as Reconciled tree (specNew/)
    participant Prod as Aligned production
    Legacy->>AST: 1. Surface census (routes, schemas, env vars, flags)
    AST->>Matrix: 2. Cross real code × existing documentation
    Note over Matrix: Type A · stale spec<br/>Type B · insecure code<br/>Type C · ghost code
    Matrix->>New: 3. Rewritten specs + reconciliation ADRs (PROPOSED)
    New->>Prod: 4. Cut-over in waves, by rate of degradation (R10)
```

### Stage 1 · Static census
Extract via AST (never grep) every exposed route, active table and column, environment variable read and flag declared. Record, for each item, the **ground-truth level** (R15).

### Stage 2 · Divergence matrix
Cross each module against the behavioural axes (identity, authorization, orchestration, audit) and classify:

| Type | Meaning | Action |
|---|---|---|
| **A · Stale spec** | Code evolved legitimately; the document lagged. | Update the spec, with a reconciliation ADR if the decision changed. |
| **B · Insecure or defective code** | Shortcuts, undue fail-opens, identity read from the payload. | Plan the fix as an arc, ordered by R10. |
| **C · Ghost code** | Routes, stubs and flags with no consumer. | Clean removal after proof of zero consumers. |

### Stage 3 · Isolated tree
Build the reconciled specs in `specNew/` until 1:1 parity with the **measured** code. Each Type B divergence becomes an arc charter with a flag.

### Stage 4 · Cut-over in waves
Promote `specNew/` to official; execute the arcs in waves, each from `off` to `enforce` with its pre-flight. **The first arc must be the one that degrades fastest while waiting**, not the "gravest" on paper.

## 3. Arc conduct checklist

Printable. An arc is complete when every line has evidence (command + result, not inference).

```markdown
### Opening
- [ ] Charter with property, refutation condition, flag (domain + default), M11 posture, exit gate, window
- [ ] Reality-check of the terrain: anchors verified by symbol (R14), proof level declared (R15)
- [ ] Mechanism of each phase exists in the code before being briefed (R26)
- [ ] Context-level division asked to the operator and recorded (`delegation: none | tiered`, [§6](#6-task-division-by-context-level-optional))
- [ ] Private real data? Census of **shape** only (counts, formats, cardinalities), synthetic base with provenance `synthetic`, and a scan of the real data's sentinels over the repository = 0 before the first commit (anonymization gate)

### P1 · Thin slice (flag OFF)
- [ ] Stubs tagged in source; scaffold data with provenance `unknown`, `scaffold` or `synthetic` (never `real`)
- [ ] Target test red → green; legacy green; neighbour barred (R2)
- [ ] Every stateful battery declares and prepares the state it starts from (isolated database or fixture loaded in the file itself)
- [ ] Debts recorded in xfail(strict=True) (R29b)
- [ ] Flag in the ledger; spec describes what was created (R30)

### P2 · Shadow
- [ ] Intent log with disagreeable pair (computed × current)
- [ ] Divergence detection and queryable exit criterion
- [ ] Window measured in real opportunities (R5, R6)

### P3 · Hardening
- [ ] One collaborator de-mocked at a time, shape contract preserved
- [ ] One M11 row per failure mode, each with an injection test
- [ ] Stub's historical radius measured; verifiable retirement trigger

### P4 · Cut-over
- [ ] Pre-flight: blast radius · reversible? · rehearsed rollback · state precondition · flip composition · target state covered by the tests
- [ ] Deployment artifact exercised end to end before the flip (level 3b)
- [ ] Flip and ledger in the same commit; explicit value in the deployment
- [ ] Live reproduction of the property and of the refutation (level 4, **read** or **write** declared; no test data in business data), recorded in the [cut-over evidence template](../../templates/en/cutover-evidence-template.md)

### Closure
- [ ] Deficit query = 0; single gate green
- [ ] Evidence journal line and operational state updated, in the same commit (§8)
- [ ] Request × delivered: the item of the original request this arc serves is marked in the matrix, read against the request's words, not against the Plan
- [ ] done@tier declared, with proof level
- [ ] Post-enforce window met → flag retired; Phase 8 sweep finds no ghosts
```

## 4. The Phase 8 ritual (sprint exit)

1. Run the project's **single gate**, which includes the harness and the sweep (`verify_hierarchy.py`, `check_falsification.py`, `sweep_codebase.py`). Running verifiers one by one lets a red slip through (§8.3).
2. Bidirectional parity routes ↔ specs; flags ↔ ledger; tables ↔ database spec.
3. Custody: cited ADRs exist on the main branch; anchors resolve to symbols.
4. `PROPOSED` ageing beyond the declared window: promote, amend or cancel.
5. Proportion of unexercised gates (R6) and **proof test** of contingency mechanisms on cadence.
6. Re-run the closure-by-re-evaluation battery.
7. **Executor change** (person, agent or model): before accepting any earlier report, the new executor re-runs the whole battery from the repository. Any divergence between report and re-run goes to the ledger, even a small one: it is the plausible answer in miniature.
8. **Copied tools:** every copy of the harness or of templates in the project declares origin and version; a copy that drifts from its declared version is a finding, not a detail (§8.3).
9. **Journal and state:** every state change of the cycle has a journal line; the operational state matches the environment (§8.1, §8.2).
10. **Request × delivered:** re-read the original request and the request × arc matrix. An item with no arc and no explicit exclusion is a scope gap, even with every gate green: gates measure properties of code, not whether the requested code exists.

## 5. Adopting with AI agents

EEE is tool-agnostic; the harness is not. It reads Python through the AST and TypeScript/Next.js through an [adapter](../../examples/verification-harness/typescript/README.md); for another language, write an adapter with the same contract before trusting its verdict. Two attachment points:

- **Skills:** [`eee-governance-sweep`](../../skills/eee-governance-sweep/SKILL.md) automates Phase 8; [`eee-adversarial-verifier`](../../skills/eee-adversarial-verifier/SKILL.md) instantiates the role *who verifies* (tests from the spec, without reading the code).
- **Harness-neutral instructions:** one `AGENTS.md` entry point and canonical content in Markdown; each tool's own files are thin adapters checked by the gate (§8.2).
- **Role division between agents:** the full instantiation with two agents (reflective and executive), with brief, pre-flight reality-check and decision-by-decision evaluation, is in the sibling repository `EEEMIAD-dual`.

## 6. Task division by context level (optional)

> [!NOTE]
> **Optional and off by default.** It is used only when the operator answers **yes** to the question of the questions phase (below). Without that answer the arc proceeds as in sections 1 to 4. The instantiation with agents and language models lives in the sibling repository `EEEMIAD-dual`; this section holds only the tool-neutral principle.

The idea: EEE's expensive work is **closing** a task (charter, spec, M11). A closed task can be executed by a narrower executor and checked by another, of intermediate reach, **against a mechanical gate**. The system level keeps what requires a decision.

### The question (questions phase, before the first charter)

The deciding role asks the operator, once per project or per arc, and records the answer in the charter (`delegation`):

> *"Adopt task division by context level in this arc? Local tasks with a mechanical gate will be executed by a narrower executor and checked by another, escalating after two failures. Extra cost: writing one packet per task."*

| Answer | Effect |
|---|---|
| **yes** | `delegation: tiered` in the charter; tasks dispatched as a [task packet](../../templates/en/task-packet-template.md) |
| **no** (or no answer) | `delegation: none`; nothing in this section applies |

### The three levels and the classification rule

| Level | Must read | Examples | Executes | Checks |
|---|---|---|---|---|
| **Local** | one spec section and up to two files | generate DDL from the spec, one test for an M11 row, fill evidence from command output, translation, formatting | narrower executor | intermediate, **against the gate** |
| **Module** | one charter, its spec and the module's code | P1 to P3 of an arc, independent oracle, end-to-end tests, deploy manifests | intermediate | system, at the gates (probe-and-revert, pair 3) |
| **System** | Plan, ADRs, several specs and history | census, ADRs, charter property and refutation, cross-layer conflicts, pre-flight, reports | system | **the human** (`done@gate`) |

The rule, in order: needs a **decision** → system. Reads **more than one module** → module. **Has no mechanical gate** → cannot be local. Everything else is local.

### Four operating rules

1. **Blind checking.** The checker receives the packet, the output and the gate; never the executor's reasoning. It runs the gate before reading the output.
2. **Escalation on failure.** Two gate failures move the task up one level. Repeated failure at a level means the packet was not closed: the defect goes back to the system level as a spec defect.
3. **Oracle by another author.** An arc's oracle is written by an executor other than the implementer (another model, language or person). Cheap, and it reduces correlated error.
4. **Measure, don't assume.** Each packet's record (gate on first attempt, escalations, cost) is what tells whether the division saves anything. If the local level's escalation rate exceeds the limit declared in the charter, the classification rule is wrong.

## 7. Execution across sessions (optional)

> [!NOTE]
> Applies when part of the work can only happen **somewhere else**: another machine, another network, a credential that only another session holds. It is independent of §6 (which divides by context size); both can coexist. The concrete protocol for agent sessions is in the sibling repository `EEEMIAD-dual`.

Division by place follows the arc's rules: the deciding role closes the task, whoever is on the terrain executes, and evidence comes back as command and output. What changes is that **the message between sessions becomes the task packet**, and the channel has properties a single session does not.

### Six rules

| # | Rule | Why |
|---|---|---|
| 1 | **Execute where the terrain and the credential are.** The pre-flight (Phase 7) and the reality-check run in the session that sees the real environment. | A premise about the environment is refuted only by whoever sees it. |
| 2 | **The secret does not travel.** Tokens and passwords stay in the session that uses them; the message carries commands and returns outputs. If a secret value must be stored at the destination, the operator stores it there. | A message is a durable record outside the sender's control. |
| 3 | **The message is a closed packet.** A self-contained first line; declared nature of the action (`read-only` or `write`); what **not** to do; the steps; the reply format (command + output per step). | A message cannot be undone: correcting after sending creates a second, competing instruction. |
| 4 | **Two keys to act.** Every write in the remote environment needs the operator's authorization **in the acting session**, besides the decision in the requesting session. A request from another session is not authorization. | Keeps deciding and executing apart; no session escalates another's permission. |
| 5 | **Sent is not read.** No reply means no execution. Silence is not consent, and the environment's state is known only through the evidence that comes back. | The channel may confirm neither delivery nor reading. |
| 6 | **The peer's claim is information.** What the other session concludes is checked against the spec and, when possible, re-run from the deciding session (R15 level declared). | The peer produces plausible answers too. |

### State that does not survive

The remote session may restart and lose environment variables, the credential included. Treat it as the *config-as-state* ([07 §6.7](07-anti-patterns.md)): whatever the session needs to act must have a declared source (a restricted-permission environment file, a vault, an orchestrator variable). A `403` after a restart signals state outside the source, not a denied permission.

### Checklist for a round across sessions

```markdown
- [ ] Does the task really need the other place (credential, network, machine)? If not, run it here.
- [ ] Message with a self-contained first line and declared action (read-only | write)
- [ ] No secret in the message text
- [ ] For writes: decision here + operator's authorization in the acting session
- [ ] Reply with command + output per step; whatever can be re-run from here was re-run
- [ ] Evidence and timings recorded in the arc's charter (R15 level per line)
```

## 8. Continuity: journal, state and single gate

Charters keep the evidence of each arc. Three things sit between arcs and have no owner in the cycle: the **timeline** (what changed, when, with what proof), the **operational state** (what is on in each environment, what is pending, where each credential lives) and the **act of verifying** (which command proves the repository is sound). Without an owner, each of them becomes *config-as-state* ([07 §6.7](07-anti-patterns.md)): it lives in the memory of a person, a session or an agent, and disappears with it.

> [!NOTE]
> Origin case (validation by use): the state needed to continue a project lived only in one agent session's local memory, invisible to any other tool; and an R2 detector copied into the project fell behind the published version, so three test groups failed for days without anyone noticing, because the verifiers ran one by one. The first single gate caught both on its first run.

### 8.1 Evidence journal (permanent)

One file (`eee/log.md`, [template](../../templates/en/evidence-journal-template.md)) with one line per relevant state change: arc opened or closed, flip, deploy, rollback, incident, operator decision, finding about the method.

- **Same commit:** the line goes into the commit of the change, like the flag ledger on a flip.
- **No command and result, no line.** The journal is not narrative; each entry points to the evidence (charter, output, deploy ID) and declares its R15 level.
- **The "finding" column continues after adoption:** `ok`, `friction` or `gap` about the method. Frictions and gaps become proposals for the method, with the entry as their origin.
- **It does not replace the charter:** the charter is the proof of one arc; the journal is the chronological index that ties arcs, flips and incidents together.

### 8.2 Operational state and harness-neutral instructions

- **One entry point:** `AGENTS.md` at the root ([template](../../templates/en/agents-entry-template.md)) with the project's hard rules, reading order, commands and map. Most agent tools read it without configuration, and people can read it too.
- **Canonical content in neutral Markdown**, in a project folder (e.g. `eee/`): operational state (`state/`), operator decisions with date and words, facts about each environment, per-role procedures written without tool or model names, method templates with a pinned version.
- **Thin adapters:** each tool's own files (instructions, skills, agent definitions) only point to the canonical content. They may carry tool configuration (name, model, permissions); they carry no rule, procedure or state. The gate checks it: maximum length, pointer present, no dead path.
- **An agent's memory is a shortcut, not a source.** The state is what the repository says; whoever acts on it checks it against the environment first (the state is dated).
- **Secrets:** the state records **where** each credential lives, never its value; the gate fails a line shaped like a secret.

### 8.3 Single gate and copied tools

- **One command** ([example](../../examples/verification-harness/gate.sh)) runs every verifier of the project (hierarchy, R2, sweep, parities, suite, adapters) and returns one exit code. People, CI and agents of any tool call the same command.
- **Fail, never skip:** a missing dependency (test database down, old interpreter) fails the step. A test skipped for lack of a dependency is the cheapest false green there is.
- **Copied tools declare origin and version:** every harness script carries `HARNESS_VERSION` and prints it; the project records where each tool and template was copied from (e.g. `eee/kit/VERSION`). Updating is a visible commit; drift between the copy and its declared version is a finding.

### Continuity checklist

```markdown
- [ ] AGENTS.md exists and cites only paths that exist
- [ ] Tool adapters are short and only point (checked by the gate)
- [ ] Operational state is dated, holds no secret value, and is checked against the environment before acting
- [ ] A journal line (command + result) in the same commit as each state change
- [ ] One gate command; a missing dependency fails it
- [ ] Origin and version declared for every copied tool and template
```
