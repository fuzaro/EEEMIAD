#!/usr/bin/env python3
"""
EEEMIAD Hierarchy of Truth Verifier for TypeScript / Next.js App Router projects.

Same contract as ../verify_hierarchy.py, adapted to file-system routing:
1. Code -> Spec: every `export (async) function GET|POST|PUT|PATCH|DELETE` (or `export const GET =`)
   in `<api-root>/**/route.ts` is named in some spec as `METHOD /api/...` ([id] maps to {id}).
2. Spec -> Code: every `METHOD /api/...` named in a spec has a route file exporting that method
   (bidirectional parity; skipped with --allow-missing-code during Phase 2).
3. Spec -> ADR: every spec has `governing_adr` (path or ADR-NNN) resolving to an ADR file;
   files whose name contains `ledger` are registers and are exempt.
4. ADR -> Plan: valid `status`, `justified_by` resolving to a Plan file.
5. Flags: every `*_MODE` flag in the ledger is declared in the flags module, and vice versa.

Usage:
  python3 verify_hierarchy_ts.py --project-root . \
      [--api-root app/src/app/api] [--flags-file app/src/server/flags.ts] [--allow-missing-code]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Version of the EEEMIAD harness this file belongs to. A project that copies the file keeps this line and
# records the origin and version (ch. 08 §8.3); a copy that drifts from its declared version is a finding.
HARNESS_VERSION = "1.5.0"

VALID_STATUS = {"PROPOSED", "ACCEPTED", "REJECTED", "DEPRECATED", "SUPERSEDED"}
METHODS = "GET|POST|PUT|PATCH|DELETE"


def parse_metadata(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S) or re.search(r"```ya?ml\s*\n(.*?)\n```", text, re.S)
    meta: dict = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.lstrip().startswith(("-", "#")):
                k, v = line.split(":", 1)
                meta[k.strip()] = v.split(" #", 1)[0].strip().strip("\"'")
    return meta


def md_paths(v: str) -> list[str]:
    return re.findall(r"[\w./-]+\.md", v or "")


def adr_ids(v: str) -> list[str]:
    return re.findall(r"\bADR-\d+\b", v or "")


def route_path(api_root: Path, f: Path) -> str:
    rel = f.parent.relative_to(api_root).as_posix()
    rel = re.sub(r"\[([^\]]+)\]", r"{\1}", rel)
    return "/api" if rel == "." else "/api/" + rel


def code_routes(api_root: Path) -> list[tuple[str, str, str]]:
    out = []
    for f in sorted(api_root.glob("**/route.ts")):
        src = f.read_text(encoding="utf-8")
        for m in re.finditer(r"export\s+(?:async\s+)?function\s+(" + METHODS + r")\b", src):
            out.append((m.group(1), route_path(api_root, f), str(f)))
        for m in re.finditer(r"export\s+(?:const|let)\s+(" + METHODS + r")\s*=", src):
            out.append((m.group(1), route_path(api_root, f), str(f)))
    return out


def spec_routes(specs: dict[str, str]) -> list[tuple[str, str, str]]:
    out = []
    for name, text in specs.items():
        for m in re.finditer(r"`(" + METHODS + r")\s+(/api[^`\s?]*)", text):
            out.append((m.group(1), m.group(2), name))
    return out


def norm(p: str) -> str:
    return re.sub(r"\{[^}]+\}", "{}", p.rstrip("/"))


def instance_of(concrete: str, pattern: str) -> bool:
    """`/api/x/por-expurgo` is an instance of `/api/x/{}`: same length, literal segments equal."""
    a, b = norm(concrete).split("/"), norm(pattern).split("/")
    return len(a) == len(b) and all(y == "{}" or x == y for x, y in zip(a, b))


def main() -> int:
    ap = argparse.ArgumentParser(description="EEEMIAD hierarchy verifier (TypeScript)")
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--api-root", default="app/src/app/api")
    ap.add_argument("--flags-file", default="app/src/server/flags.ts")
    ap.add_argument("--allow-missing-code", action="store_true")
    a = ap.parse_args()
    root = Path(a.project_root)
    api_root, flags_file = root / a.api_root, root / a.flags_file
    adr_dir = next((root / d for d in ("Plan/decisions", "adr") if (root / d).exists()), None)
    spec_dir = next((root / d for d in ("specs", "spec") if (root / d).exists()), None)
    issues: list[str] = []
    print(f"[*] EEEMIAD harness {HARNESS_VERSION} (verify_hierarchy_ts.py)")
    print(f"[*] Hierarchy of truth (TypeScript) at {root.resolve()}")

    adrs: dict[str, dict] = {}
    if adr_dir is None:
        issues.append("Missing ADR directory (Plan/decisions/ or adr/)")
    else:
        for f in sorted(adr_dir.glob("*.md")):
            meta = parse_metadata(f.read_text(encoding="utf-8"))
            adrs[f.name] = meta
            if meta.get("status") not in VALID_STATUS:
                issues.append(f"ADR {f.name}: status missing or invalid ({meta.get('status')!r})")
            elif meta["status"] == "PROPOSED":
                print(f"    [i] {f.name} is PROPOSED (valid in Phase 2; an arc charter requires ACCEPTED)")
            refs = md_paths(meta.get("justified_by", ""))
            if not refs:
                issues.append(f"ADR {f.name}: no justified_by pointing to a Plan file")
            for ref in refs:
                if not (root / ref).exists():
                    issues.append(f"ADR {f.name}: justified_by cites {ref}, which does not exist")

    specs: dict[str, str] = {}
    if spec_dir is None:
        issues.append("Missing specs directory (specs/ or spec/)")
    else:
        for f in sorted(spec_dir.glob("**/*.md")):
            text = f.read_text(encoding="utf-8")
            specs[f.name] = text
            meta = parse_metadata(text)
            g = meta.get("governing_adr", "")
            paths, ids = md_paths(g), adr_ids(g)
            if not paths and not ids:
                if "ledger" not in f.stem.lower():
                    issues.append(f"Spec {f.name}: no governing_adr")
            for ref in paths:
                if not (root / ref).exists():
                    issues.append(f"Spec {f.name}: governing_adr {ref} does not exist")
            for ident in ids:
                if not any(n.startswith(ident) for n in adrs):
                    issues.append(f"Spec {f.name}: governing_adr {ident} matches no ADR file")
            if meta.get("status", "").lower() == "draft":
                issues.append(f"Spec {f.name}: status Draft (violates living parity)")

    sr = spec_routes(specs)
    cr = code_routes(api_root) if api_root.exists() else []
    spec_set = {(m, norm(p)) for m, p, _ in sr}
    code_set = {(m, norm(p)) for m, p, _ in cr}
    if not api_root.exists():
        msg = f"API root {a.api_root} not found: no code route was examined"
        if a.allow_missing_code:
            print(f"    [i] {msg} (allowed by --allow-missing-code)")
        else:
            issues.append(msg)
    for m, p, f in cr:
        if (m, norm(p)) in spec_set:
            print(f"    [+] code→spec OK: {m} {p}")
        else:
            issues.append(f"Route in code without spec: {m} {p} ({f})")
    missing = sorted({(m, p) for m, p, _ in sr
                      if (m, norm(p)) not in code_set and not any(cm == m and instance_of(p, cp) for cm, cp in code_set)})
    for m, p in missing:
        if a.allow_missing_code:
            print(f"    [i] Route in spec without code (allowed in Phase 2): {m} {p}")
        else:
            issues.append(f"Route in spec without code: {m} {p}")

    ledger_text = next((t for n, t in specs.items() if "ledger" in n.lower()), "")
    ledger_flags = set(re.findall(r"^\| `([A-Z][A-Z0-9_]*_MODE)`", ledger_text, re.M))
    code_flags = set(re.findall(r"\b([A-Z][A-Z0-9_]*_MODE)\b", flags_file.read_text(encoding="utf-8"))) if flags_file.exists() else set()
    if flags_file.exists():
        for fl in sorted(ledger_flags - code_flags):
            issues.append(f"Flag in ledger not declared in {a.flags_file}: {fl}")
        for fl in sorted(code_flags - ledger_flags):
            issues.append(f"Flag in {a.flags_file} without a ledger row: {fl}")
    elif ledger_flags:
        print(f"    [i] {a.flags_file} not found; {len(ledger_flags)} ledger flag(s) await a consumer")

    print("\n--- Summary ---")
    print(f"    examined: {len(adrs)} ADR(s), {len(specs)} spec(s), {len(cr)} code route(s), {len(set((m, norm(p)) for m, p, _ in sr))} spec route(s), {len(ledger_flags)} ledger flag(s)")
    if issues:
        print(f"[!] FAILED: {len(issues)} issue(s):")
        for i in issues:
            print(f"    - ❌ {i}")
        return 1
    print("[+] SUCCESS: no integrity issue found in what was examined (counts above).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
