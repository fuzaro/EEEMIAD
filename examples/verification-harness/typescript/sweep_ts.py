#!/usr/bin/env python3
"""
EEEMIAD Phase 8 sweep for TypeScript projects (counterpart of skills/eee-governance-sweep).

- Ghost flags: `*_MODE` flags declared in the flags module with zero consumers elsewhere.
  A flag whose ledger row has no arc evidence yet ("—" in the last column) is reported as
  "awaiting its arc", not as a ghost: between the charter and P1 every flag is consumer-less by design.
- Ledger ↔ code: flags in the ledger and not in code, and vice versa.
- Forbidden symbols: identity read from the payload or from custom headers (configurable).
- Environment variables read in code (`process.env.X`) without a line in the deploy spec.

Usage:
  python3 sweep_ts.py --src app/src --specs specs \
      [--flags-file app/src/server/flags.ts] [--deploy-spec specs/deploy.md] \
      [--forbid 'x-user' --forbid 'body\\.user']
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Version of the EEEMIAD harness this file belongs to. A project that copies the file keeps this line and
# records the origin and version (ch. 08 §8.3); a copy that drifts from its declared version is a finding.
HARNESS_VERSION = "1.7.0"

DEFAULT_FORBIDDEN = [r"['\"]x-user['\"]", r"['\"]x-role['\"]", r"body\.user\b", r"body\.subject\b", r"body\.autor\b"]
IGNORED_ENV = {"NODE_ENV"}


def main() -> int:
    ap = argparse.ArgumentParser(description="EEEMIAD Phase 8 sweep (TypeScript)")
    ap.add_argument("--src", default="app/src")
    ap.add_argument("--specs", default="specs")
    ap.add_argument("--flags-file", default=None, help="default: <src>/server/flags.ts")
    ap.add_argument("--deploy-spec", default=None, help="default: <specs>/deploy.md")
    ap.add_argument("--forbid", action="append", default=None, help="regex of a forbidden symbol (repeatable)")
    a = ap.parse_args()
    print(f"[*] EEEMIAD harness {HARNESS_VERSION} (sweep_ts.py)")
    src, specs = Path(a.src), Path(a.specs)
    flags_file = Path(a.flags_file) if a.flags_file else src / "server" / "flags.ts"
    deploy_spec = Path(a.deploy_spec) if a.deploy_spec else specs / "deploy.md"
    forbidden = a.forbid or DEFAULT_FORBIDDEN
    issues: list[str] = []

    corpus = {f: f.read_text(encoding="utf-8") for f in src.glob("**/*.ts*") if "node_modules" not in f.parts}
    declared = set(re.findall(r"\b([A-Z][A-Z0-9_]*_MODE)\b", corpus.get(flags_file, ""))) if flags_file.exists() else set()
    ledger_path = next((p for p in specs.glob("**/*.md") if "ledger" in p.stem.lower()), None)
    ledger = ledger_path.read_text(encoding="utf-8") if ledger_path else ""
    rows = {m.group(1): m.group(0) for m in re.finditer(r"^\| `([A-Z][A-Z0-9_]*_MODE)`.*$", ledger, re.M)}

    print(f"[*] flags declared in {flags_file}: {sorted(declared)}")
    for fl in sorted(declared):
        consumers = [f for f, c in corpus.items() if f != flags_file and re.search(r"\b" + fl + r"\b", c)]
        if consumers:
            print(f"    [+] {fl}: {len(consumers)} consumer(s)")
        elif fl in rows and rows[fl].rstrip().rstrip("|").rstrip().endswith("—"):
            print(f"    [i] {fl}: no consumer yet, ledger shows no arc evidence (awaiting its arc)")
        else:
            issues.append(f"ghost flag: {fl} declared with no consumer")
    for fl in sorted(set(rows) - declared):
        issues.append(f"flag in the ledger not declared in code: {fl}")
    for fl in sorted(declared - set(rows)):
        issues.append(f"flag in code without a ledger row: {fl}")

    for f, c in corpus.items():
        for pat in forbidden:
            for m in re.finditer(pat, c):
                issues.append(f"forbidden symbol /{pat}/ at {f}:{c[: m.start()].count(chr(10)) + 1} (identity from the payload?)")

    deploy = deploy_spec.read_text(encoding="utf-8") if deploy_spec.exists() else ""
    env_vars = set()
    for c in corpus.values():
        env_vars |= set(re.findall(r"process\.env\.([A-Z_][A-Z0-9_]*)", c))
    for v in sorted(env_vars - IGNORED_ENV):
        if f"`{v}`" not in deploy:
            issues.append(f"environment variable {v} read in code without a line in {deploy_spec}")
    print(f"[*] environment variables read: {sorted(env_vars)}")

    print("\n--- Phase 8 summary ---")
    if issues:
        print(f"[!] {len(issues)} finding(s):")
        for i in issues:
            print(f"    - ❌ {i}")
        return 1
    print("[+] SUCCESS: no ghost flag, no forbidden symbol, every env var specified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
