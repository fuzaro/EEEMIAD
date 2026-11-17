#!/usr/bin/env python3
"""
EEEMIAD Rule R2 (Disagreeable Pairs) & Negative Control Verifier (pytest)

Inspects test files with the AST and checks that every **group** of tests that asserts something
positive also carries at least one negative control (a case that must be refused, fail or diverge).

A group is a test class; tests outside any class form one group per file. Counting per group,
not per file, prevents one negative test in a large file from vouching for unrelated positives.

Declared debts (R29b) are tests marked `@pytest.mark.xfail(strict=True)`. They are counted and
listed separately: they are neither positive nor negative evidence, they are announced obligations.
A non-strict `xfail` is reported as a problem, because an unexpected pass would go unnoticed.

Classification still relies on test names (the vocabulary below): name the refusal in the test.
This is a cheap proxy for R2, not a proof of it; the pair itself is defined in ch. 06 §4.
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

# Version of the EEEMIAD harness this file belongs to. A project that copies the file keeps this line and
# records the origin and version (ch. 08 §8.3); a copy that drifts from its declared version is a finding.
HARNESS_VERSION = "1.5.0"

NEGATIVE = re.compile(
    r"invalid|fail|deny|denie|reject|refuse|unauth|forbid|malform|negative|blocked|barred|abort|"
    r"diverg|tamper|corrupt|missing|unknown|neighbo|refut|stale|_(400|401|403|404|409|422|500|503)(_|$)",
    re.I,
)


def _xfail_kind(fn: ast.AST) -> str | None:
    """'strict' | 'loose' | None for a pytest.mark.xfail decorator."""
    for deco in getattr(fn, "decorator_list", []):
        target = deco.func if isinstance(deco, ast.Call) else deco
        if isinstance(target, ast.Attribute) and target.attr == "xfail":
            if isinstance(deco, ast.Call):
                for kw in deco.keywords:
                    if kw.arg == "strict" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                        return "strict"
            return "loose"
    return None


def analyze_test_file(filepath) -> dict[str, dict[str, list[str]]]:
    """Return {group: {pos, neg, debt, loose}} for one test file."""
    tree = ast.parse(Path(filepath).read_text(encoding="utf-8"), filename=str(filepath))
    groups: dict[str, dict[str, list[str]]] = {}

    def add(group: str, fn: ast.AST) -> None:
        g = groups.setdefault(group, {"pos": [], "neg": [], "debt": [], "loose": []})
        name = fn.name  # type: ignore[attr-defined]
        kind = _xfail_kind(fn)
        if kind == "strict":
            g["debt"].append(name)
        elif kind == "loose":
            g["loose"].append(name)
        elif NEGATIVE.search(name):
            g["neg"].append(name)
        else:
            g["pos"].append(name)

    module_group = f"{Path(filepath).name} (module)"
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
            add(module_group, node)
        elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name.startswith("test_"):
                    add(f"{Path(filepath).name}::{node.name}", item)
    return groups


def verify_falsification(test_dir) -> int:
    print(f"[*] EEEMIAD harness {HARNESS_VERSION} (check_falsification.py)")
    print(f"[*] Checking EEEMIAD Rule R2 (disagreeable pairs, per group) across: {test_dir}")
    test_path = Path(test_dir)
    if not test_path.exists():
        print(f"[-] Directory {test_dir} not found.")
        return 1

    total = {"pos": 0, "neg": 0, "debt": 0}
    unpaired: list[str] = []
    loose: list[str] = []
    files = [f for f in sorted(test_path.glob("**/*.py")) if f.name.startswith("test_") or f.name.endswith("_test.py")]
    for f in files:
        for group, g in analyze_test_file(f).items():
            for k in total:
                total[k] += len(g[k])
            print(f"    - {group}: {len(g['pos'])} positive, {len(g['neg'])} negative, {len(g['debt'])} declared debt")
            for d in g["debt"]:
                print(f"        · debt (xfail strict): {d}")
            if g["pos"] and not g["neg"]:
                unpaired.append(group)
            loose += [f"{group}::{n}" for n in g["loose"]]

    print(f"\n[+] positive {total['pos']} · negative {total['neg']} · declared debts {total['debt']}")
    status = 0
    if total["pos"] == 0 and total["neg"] == 0:
        print("[!] No tests found.")
        return 1
    if unpaired:
        print(f"[!] {len(unpaired)} group(s) with positive tests and no negative control (R2):")
        for u in unpaired:
            print(f"    - ❌ {u}")
        status = 1
    if loose:
        print(f"[!] {len(loose)} non-strict xfail(s): an unexpected pass would go unnoticed (use strict=True, R29b):")
        for n in loose:
            print(f"    - ❌ {n}")
        status = 1
    if status == 0:
        print("[+] SUCCESS: every group with positive tests carries at least one negative control.")
    return status


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EEEMIAD Rule R2 Negative Control Verifier")
    parser.add_argument("--test-dir", default="./tests", help="Directory containing test files")
    args = parser.parse_args()
    sys.exit(verify_falsification(args.test_dir))
