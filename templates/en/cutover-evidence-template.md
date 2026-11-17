# 🚦 CUT-OVER EVIDENCE · [Arc] · [off → enforce]

*Record of one flag flip: the pre-flight answered, the artifact exercised and the live reproduction, each line with command and result*

```yaml
arc_id: ARC-[XXX]
flag: [FLAG_NAME]
transition: [off → shadow | shadow → enforce | enforce → shadow]
environment: [environment name]
artifact: [image@tag or package@version]
code_commit: [short sha of the code in the artifact]
flip_commit: [sha of the commit that changes manifest + ledger]
decided_by: [deciding role]
date: YYYY-MM-DD
```

---

> [!IMPORTANT]
> A line without a command and its observed output is inference and does not count. Proof level (R15) declared in each section.

## 1. Pre-flight answered (ch. 04, Phase 7)

| # | Question | Command | Observed output |
|---|---|---|---|
| 1 | Side effects beyond the target | | |
| 2 | Reversible? (if NO → stop) | | |
| 3 | Rollback rehearsed, with measured time | | |
| 4 | State precondition at the source (tables, grants, variables, registry reachable by the nodes) | | |
| 5 | Composition: other gates changed in this window and their product exercised | | |
| 6 | `enforce` mechanism exists (syntactic check) | | |
| 7 | Target state covered by the tests? (empty, just migrated, old data outside a new rule, volume) If not, battery run from that state | | |

## 2. Deployment artifact exercised (level 3b)

The artifact **that ships**, not the test process.

| Check | Command | Result |
|---|---|---|
| Boots without error and with the expected flags | | |
| Health publishes flags = ledger | | |
| Happy path of the property | | |
| Neighbour that must stay barred (R2) | | |

## 3. Live reproduction (level 4)

Mode: **read** | **write** (a write into an environment holding business data only with data marked as test and removable; otherwise the write is proven at 3b and this level covers reads only).

| Case | Request | Expected | Observed |
|---|---|---|---|
| **Property** | | | |
| **Refutation** (the case that, if it passed, would refute the arc) | | barred | |

## 4. Flip and ledger

- Single commit changing manifest and ledger: `[sha]`
- Explicit value in the manifest: `[FLAG]="[value]"` at `[file:line]`
- Health after the flip: `[output]`

## 5. Observation window

- Start: `YYYY-MM-DD HH:MM` · declared size: `[N real opportunities]`
- Exit-criterion query: `[command]` → `[total, divergent]`

## 6. Decision

`done@[tier]`, proof level `[3b | 4]`, decided by `[role]` on `YYYY-MM-DD`. Flag retirement: after the window, with proof of zero consumers.
