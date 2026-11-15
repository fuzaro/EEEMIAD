# 📦 TASK PACKET · [ID]

*Dispatch unit of the context-level division: one closed task, with declared inputs, output and gate*

> [!NOTE]
> Used **only** when the operator accepted the context-level division at the questions phase ([08 §6](../../docs/en/08-application-guide.md#6-task-division-by-context-level-optional)). The system level writes the packet; the executor and the checker do not change it.

```yaml
packet_id: [ARC-XXX-T01]
arc: ARC-[XXX]
level: local          # local | module | system (classification rule in 08 §6)
written_by: [system-level role/agent]
executor: [executing role/agent]
checker: [checking role/agent; never the executor's author]
escalate_after: 2     # gate failures before moving up one level
```

---

## 1. Objective (one verifiable sentence)

> *"[What comes to exist or change, in observable terms.]"*

## 2. Allowed inputs

| File | Section | Why |
|---|---|---|
| `specs/[component].md` | §[n] | contract |
| `[path]` | `[symbol or lines]` | change point |

Nothing outside this list is read by the executor. If the task needs another read, it does not belong to this level: send it back with the reason.

## 3. Forbidden reads

- For the checker: the implementation and the executor's reasoning. It receives only this packet, the output and the gate.
- [others, e.g. real data, secrets]

## 4. Output contract

| Output | Shape | Where |
|---|---|---|
| [file/section/report] | [exact format] | [path] |

## 5. Gate (the verdict comes from this command, not from reading)

```bash
[command that decides]
```

Expected result: `[output or exit code]`.

> [!IMPORTANT]
> **A task without a mechanical gate cannot be local.** Without a deciding command the checker would have to re-read the work, which recreates single authorship.

## 6. Refutation condition

> *"[Observation that, if it occurs, shows the task was not done even with a green gate.]"*

## 7. Record (filled by the checker)

| Field | Value |
|---|---|
| Gate on first attempt | passed / failed |
| Attempts | [n] |
| Escalated to | — / [level] |
| Verdict | APPROVED · RETURNED ([reason]) · ESCALATED |
| Cost (if the tool reports it) | [tokens / time] |
