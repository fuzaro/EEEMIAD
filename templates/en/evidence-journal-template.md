# 🧪 EVIDENCE JOURNAL · [Project]

*One line per relevant state change, in the same commit as the change, always with command and result (EEEMIAD ch. 08 §8.1)*

**When to write:** arc opened or closed, flag flip, deploy, rollback, incident, operator decision, finding about the method. **No command and result, no line.**

**Finding about the method:** **ok** (the prescription worked as written) · **friction** (it worked, but cost more than it should or needed interpretation) · **gap** (the method does not cover it; a local decision was made). Frictions and gaps get a code (F1, G1…) and become proposals for the method, with this entry as their origin.

| # | Date | Context | Prescription (ch. / rule) | What was done | Evidence (command → result, R15 level) | Finding |
|---|---|---|---|---|---|---|
| 1 | YYYY-MM-DD | [ARC-XXX · flip · deploy · incident] | [e.g. ch. 04 Phase 7, pre-flight] | [what changed, in one or two sentences] | [`command` → summarised output; link to the charter or cut-over evidence; level] | **ok** |
| 2 | YYYY-MM-DD | [ARC-XXX] | [e.g. R2] | [ ] | [ ] | **friction F1** · [what it cost and why; proposal] |

<!--
Rules:
- The line goes into the commit of the change, like the flag ledger on a flip.
- The journal does not replace the charter: the charter is the proof of one arc; the journal is the chronological index across arcs.
- Do not record secret values or private data; record where they are and how to check.
- Entries are never deleted. A mistake in an old entry is corrected by a new entry that cites it.
-->
