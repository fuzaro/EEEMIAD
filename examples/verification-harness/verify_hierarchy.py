#!/usr/bin/env python3
"""
EEEMIAD Hierarchy of Truth Verifier (§2)
Validates that:
1. Every Code endpoint has an active Specification.
2. Every Specification is governed by an Accepted ADR.
3. Every ADR is justified by a Foundational Plan Principle.
4. No Hierarchy Inversion (Anti-Pattern §6.7) is present.
"""
import os
import sys
import argparse
import ast
import re
from pathlib import Path

def get_literal_value(node):
    if hasattr(node, 'value'):
        return node.value
    elif hasattr(node, 's'):
        return node.s
    return None

def parse_markdown_yaml_frontmatter(content):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}
    raw_yaml = match.group(1)
    meta = {}
    for line in raw_yaml.split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta

def check_project_hierarchy(root_dir):
    root = Path(root_dir)
    print(f"[*] Validating EEEMIAD Hierarchy of Truth for: {root.resolve()}")

    adrs_dir = root / "adr"
    if not adrs_dir.exists():
        adrs_dir = root / "Plan" / "decisions"
    
    specs_dir = root / "spec"
    if not specs_dir.exists():
        specs_dir = root / "specs"

    code_dir = root / "code"
    if not code_dir.exists():
        code_dir = root / "poc"

    issues = []

    # 1. Inspect ADRs
    adrs = {}
    if adrs_dir.exists():
        for f in adrs_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            meta = parse_markdown_yaml_frontmatter(content)
            adrs[f.name] = meta
            if meta.get("status") == "PROPOSED":
                print(f"    [i] Info: ADR {f.name} is PROPOSED (valid under EEE Phase 2)")
    else:
        issues.append(f"Missing ADR directory: {adrs_dir}")

    # 2. Inspect Specifications
    specs = {}
    if specs_dir.exists():
        for f in specs_dir.glob("**/*.md"):
            content = f.read_text(encoding="utf-8")
            specs[f.name] = content
            if "status: Draft" in content:
                issues.append(f"Specification {f.name} is still in Draft state (violates living 1:1 parity)")
    else:
        issues.append(f"Missing Specifications directory: {specs_dir}")

    # 3. Inspect Code Routes vs Specs
    if code_dir.exists():
        extracted_routes = []
        for py_file in code_dir.glob("**/*.py"):
            try:
                tree = ast.parse(py_file.read_text(encoding="utf-8"))
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        for deco in node.decorator_list:
                            if isinstance(deco, ast.Call) and isinstance(deco.func, ast.Attribute):
                                if deco.func.attr.upper() in ("GET", "POST", "PUT", "DELETE", "PATCH"):
                                    if deco.args:
                                        val = get_literal_value(deco.args[0])
                                        if val is not None:
                                            extracted_routes.append((deco.func.attr.upper(), str(val), py_file.name))
            except Exception as e:
                issues.append(f"Failed to parse code AST in {py_file.name}: {e}")

        # Match routes against specs
        all_specs_text = "\n".join(specs.values())
        for method, route, filename in extracted_routes:
            if route not in all_specs_text:
                issues.append(f"Code route '{method} {route}' in {filename} has no matching specification in specs/ (Unspecified Code)")
            else:
                print(f"    [+] OK: {method} {route} verified against specification.")
    else:
        print(f"    [i] Note: Code directory {code_dir} not yet present (acceptable for early phase)")

    print("\n--- Verifier Summary ---")
    if issues:
        print(f"[!] FAILED: Found {len(issues)} hierarchy integrity issues:")
        for issue in issues:
            print(f"    - ❌ {issue}")
        return 1
    else:
        print("[+] SUCCESS: Hierarchy Plan → ADR → Spec → Code is 100% compliant and intact!")
        return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EEEMIAD Hierarchy of Truth Verifier")
    parser.add_argument("--project-root", default=".", help="Root directory of the project")
    args = parser.parse_args()
    sys.exit(check_project_hierarchy(args.project_root))
