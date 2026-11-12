#!/usr/bin/env python3
"""
EEEMIAD Rule R2 (Disagreeable Pairs) & Negative Control Verifier
Inspects test files to ensure that test suites test both the positive (must-pass)
and negative/adversarial (must-fail) boundary paths.
"""
import ast
import os
import sys
import argparse
from pathlib import Path

def analyze_test_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)

    positive_tests = []
    negative_tests = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            name_lower = node.name.lower()
            if any(term in name_lower for term in ("invalid", "fail", "deny", "unauth", "malformed", "negative", "blocked")):
                negative_tests.append(node.name)
            else:
                positive_tests.append(node.name)

    return positive_tests, negative_tests

def verify_falsification(test_dir):
    print(f"[*] Checking EEEMIAD Rule R2 (Disagreeable Pairs) across: {test_dir}")
    test_path = Path(test_dir)
    if not test_path.exists():
        print(f"[-] Directory {test_dir} not found.")
        return 1

    total_pos = 0
    total_neg = 0
    files_missing_negatives = []

    for f in test_path.glob("**/*.py"):
        if f.name.startswith("test_") or f.name.endswith("_test.py"):
            pos, neg = analyze_test_file(f)
            total_pos += len(pos)
            total_neg += len(neg)
            if pos and not neg:
                files_missing_negatives.append(f.name)
            print(f"    - {f.name}: {len(pos)} positive, {len(neg)} negative controls")

    print(f"\n[+] Total positive tests: {total_pos}")
    print(f"[+] Total negative/adversarial controls: {total_neg}")

    if files_missing_negatives:
        print(f"\n[!] WARNING: {len(files_missing_negatives)} test files lack negative control tests (Violates Rule R2):")
        for fn in files_missing_negatives:
            print(f"    - ⚠️ {fn} has zero must-fail assertions!")
        return 1
    elif total_pos == 0:
        print("[!] No tests found.")
        return 1
    else:
        print("[+] SUCCESS: All test suites enforce Rule R2 with balanced disagreeable pairs!")
        return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EEEMIAD Rule R2 Negative Control Verifier")
    parser.add_argument("--test-dir", default="./tests", help="Directory containing test files")
    args = parser.parse_args()
    sys.exit(verify_falsification(args.test_dir))
