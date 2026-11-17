#!/usr/bin/env python3
"""
EEEMIAD Rule R2 (disagreeable pairs) for Vitest / Jest test files.

Same contract as ../check_falsification.py: every `describe` group that has positive cases must
carry at least one negative control. Declared debts (R29b) are `it.fails(` / `test.fails(`
(Vitest's counterpart of pytest `xfail(strict=True)`: the suite turns red when the debt is paid,
forcing its promotion to a normal test). `.skip` and `.todo` are reported, never counted as evidence.

Classification relies on case names: name the refusal in the test.

Usage: python3 check_falsification_ts.py --test-dir tests
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Version of the EEEMIAD harness this file belongs to. A project that copies the file keeps this line and
# records the origin and version (ch. 08 §8.3); a copy that drifts from its declared version is a finding.
HARNESS_VERSION = "1.5.0"

NEGATIVE = re.compile(
    r"reject|denie|deny|fail|invalid|unauthor|forbid|malform|blocked|barred|refuse|abort|diverg|tamper|corrupt|"
    r"missing|unknown|neighbo|refut|stale|negative control|\b(400|401|403|404|409|422|500|503)\b",
    re.I,
)


def analyze(src: str) -> dict[str, dict[str, list[str]]]:
    groups: dict[str, dict[str, list[str]]] = {}
    current = "(top level)"
    for line in src.splitlines():
        m = re.match(r"\s*describe(?:\.\w+)?\(\s*['\"`](.+?)['\"`]", line)
        if m:
            current = m.group(1)
            groups.setdefault(current, {"pos": [], "neg": [], "debt": [], "skip": []})
            continue
        m = re.match(r"\s*(?:it|test)(\.fails|\.todo|\.skip|\.skipIf\([^)]*\))?\(\s*['\"`](.+?)['\"`]", line)
        if not m:
            continue
        g = groups.setdefault(current, {"pos": [], "neg": [], "debt": [], "skip": []})
        mod, name = m.group(1) or "", m.group(2)
        if mod == ".fails":
            g["debt"].append(name)
        elif mod.startswith((".todo", ".skip")):
            g["skip"].append(name)
        elif NEGATIVE.search(name):
            g["neg"].append(name)
        else:
            g["pos"].append(name)
    return groups


def main() -> int:
    ap = argparse.ArgumentParser(description="EEEMIAD R2 verifier (Vitest/Jest)")
    ap.add_argument("--test-dir", default="tests")
    a = ap.parse_args()
    print(f"[*] EEEMIAD harness {HARNESS_VERSION} (check_falsification_ts.py)")
    files = sorted(p for ext in ("ts", "tsx", "js", "mjs") for p in Path(a.test_dir).glob(f"**/*.test.{ext}"))
    if not files:
        print("[!] no *.test.(ts|tsx|js|mjs) found")
        return 1
    unpaired, tot = [], {"pos": 0, "neg": 0, "debt": 0, "skip": 0}
    for f in files:
        for g, d in analyze(f.read_text(encoding="utf-8")).items():
            for k in tot:
                tot[k] += len(d[k])
            print(f"    - {f.name} › {g}: {len(d['pos'])} pos, {len(d['neg'])} neg, {len(d['debt'])} debt, {len(d['skip'])} skipped")
            for n in d["debt"]:
                print(f"        · declared debt: {n}")
            if d["pos"] and not d["neg"]:
                unpaired.append(f"{f.name} › {g}")
    print(f"\n[+] positive {tot['pos']} · negative {tot['neg']} · declared debts {tot['debt']} · skipped {tot['skip']} (skipped is not evidence)")
    if unpaired:
        print(f"[!] {len(unpaired)} group(s) without a negative control (R2):")
        for u in unpaired:
            print(f"    - ❌ {u}")
        return 1
    print("[+] SUCCESS: every group with positive cases carries at least one negative control.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
