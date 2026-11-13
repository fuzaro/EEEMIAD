# 🏗️ Example · An Evolutionary Arc in Pure Python

This directory is a **runnable illustration** of chapter 06 (*Evolutionary Construction*): one property, one flag, three states, and a test battery that carries the evidence through the arc. No external dependencies besides `pytest`.

| File | What it shows |
|---|---|
| `spec/audit-sink.md` | The contract the stub **and** the real adapter must satisfy (Phase 2), the flag contract, the M11 row, the exit gate. |
| `code/audit_sink.py` | The flag resolved from a declared tri-state domain; the stub with `scaffold` provenance; shadow computing divergence without deciding; enforce with fail-open durable buffer. |
| `code/tests/test_audit_sink.py` | The battery: flag contract, P1/P2/P4 behaviour, fault injection, the neighbour that must stay barred, and a declared debt in `xfail(strict=True)`. |

## Run

```bash
pip install pytest
pytest -q examples/evolutionary-arc/code/tests
```

Expected: all tests pass and **one is reported `xfailed`**. That `xfail(strict=True)` is a *declared debt* (automatic buffer drain is left to a later arc). The day someone implements automatic drain, the test turns `XPASS` and the suite fails on purpose: the debt register announces its own settlement (Rule R29b).

## What to look for

1. **The stub proves the pipe, not the measurement.** In `off`, records are tagged `scaffold`; nothing can later be read as a real measurement.
2. **Shadow does not decide.** It exercises the real path and writes a disagreeable pair (`stub_ok` vs `real_ok`) to an intent log.
3. **Posture follows the kind of thing guarded (R7).** This is an *evidence* sink, so failure is fail-open with a durable buffer. A *decision* gate would fail closed.
4. **No silent fallback.** In `enforce`, a store outage never routes to the stub; the test for that is the "neighbour stays barred" negative control.
5. **Flags are contracts.** Default `off` in code, a declared domain, and a loud boot line whenever a scaffold path is live. A value like `AUDIT_SINK_MODE=true` is an error, not a guess.

## How this maps to a real arc

| Arc step | Here | In a real system |
|---|---|---|
| Charter | `spec/audit-sink.md` §1 | `templates/*/arc-charter-template.md` filled and committed |
| P1 · thin slice, flag off | `StubSink` | stub behind the flag, explicit deploy value, ledger row |
| P2 · shadow | `intent_log` | intent log + divergence detector + exit-criterion endpoint |
| P3 · hardening | fault-injection tests | one M11 row per failure mode, each with a test |
| P4 · cut-over | `enforce` tests | pre-flight (blast radius, rollback, state precondition, flip composition) |
| Closure | `pytest` exit code 0 with 1 xfail | deficit query = 0, `done@functional` declared with ground-truth level |
