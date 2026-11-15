#!/usr/bin/env python3
"""
EEEMIAD Hierarchy of Truth Verifier (ch. 03, ch. 08 §1 step 8)

Checks, and reports how much it actually examined:
1. Code -> Spec: every route found in code (FastAPI/Flask-style decorators, via AST)
   is named in some specification.
2. Spec -> ADR: every specification declares `governing_adr` (a path, or an `ADR-NNN` identifier as in
   the arc-charter template), and it resolves to an existing ADR. Files whose name contains `ledger`
   are registers across ADRs and are exempt.
3. ADR -> Plan: every ADR has a valid `status` and a `justified_by` that resolves to a Plan file.
4. ADR -> Spec: every path listed in an ADR's `governs` exists (no ADR governing a phantom spec).

Metadata is read from a leading `---` frontmatter block or from the first ```yaml fenced block
(the form used by the EEEMIAD templates). Inline `# comments` and quotes are stripped.

A verifier that examines nothing must not report success. If no code directory is found the
run FAILS, unless `--allow-missing-code` is passed (valid during Phase 2, before any code).
The summary always states the counts examined, never a bare "100%".

Exit code: 0 when intact, 1 when any issue is found.
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

VALID_STATUS = {"PROPOSED", "ACCEPTED", "REJECTED", "DEPRECATED", "SUPERSEDED"}
HTTP_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH"}


def get_literal_value(node):
    if isinstance(node, ast.Constant):
        return node.value
    return getattr(node, "s", None)


def _clean(value: str) -> str:
    value = value.split(" #", 1)[0].strip()
    return value.strip("\"'")


def parse_metadata(content: str) -> dict:
    """Read `key: value` pairs from a `---` frontmatter or the first ```yaml block."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not m:
        m = re.search(r"```ya?ml\s*\n(.*?)\n```", content, re.DOTALL)
    if not m:
        return {}
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith(("-", "#")):
            k, v = line.split(":", 1)
            meta[k.strip()] = _clean(v)
    return meta


def md_paths(value: str) -> list[str]:
    """Paths to Markdown files cited in a metadata value (lists, anchors and § references allowed)."""
    return re.findall(r"[\w./-]+\.md", value or "")


def adr_ids(value: str) -> list[str]:
    """ADR identifiers cited without a path (`ADR-001 (status=ACCEPTED)`, the arc-charter template form)."""
    return re.findall(r"\bADR-\d+\b", value or "")


def first_existing(root: Path, *candidates: str) -> Path | None:
    for c in candidates:
        p = root / c
        if p.exists():
            return p
    return None


def resolve(root: Path, ref: str, base: Path) -> bool:
    """A cited path resolves relative to the project root or to the citing file's directory."""
    return (root / ref).exists() or (base.parent / ref).exists()


def extract_routes(code_dir: Path, issues: list[str]) -> list[tuple[str, str, str]]:
    routes = []
    for py_file in sorted(code_dir.glob("**/*.py")):
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
        except SyntaxError as e:
            issues.append(f"Failed to parse code AST in {py_file.name}: {e}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for deco in node.decorator_list:
                    if isinstance(deco, ast.Call) and isinstance(deco.func, ast.Attribute):
                        method = deco.func.attr.upper()
                        if method in HTTP_METHODS and deco.args:
                            val = get_literal_value(deco.args[0])
                            if isinstance(val, str):
                                routes.append((method, val, py_file.name))
    return routes


def check_project_hierarchy(root_dir: str, allow_missing_code: bool = False) -> int:
    root = Path(root_dir)
    print(f"[*] Validating EEEMIAD Hierarchy of Truth for: {root.resolve()}")
    issues: list[str] = []

    adrs_dir = first_existing(root, "adr", "Plan/decisions")
    specs_dir = first_existing(root, "spec", "specs")
    code_dir = first_existing(root, "code", "poc", "src")
    plan_dir = first_existing(root, "plan", "Plan/docs", "Plan")

    # ADRs
    adrs: dict[str, dict] = {}
    adr_files: dict[str, Path] = {}
    if adrs_dir is None:
        issues.append("Missing ADR directory (adr/ or Plan/decisions/)")
    else:
        for f in sorted(adrs_dir.glob("*.md")):
            meta = parse_metadata(f.read_text(encoding="utf-8"))
            adrs[f.name] = meta
            adr_files[f.name] = f
            status = meta.get("status")
            if status not in VALID_STATUS:
                issues.append(f"ADR {f.name}: status missing or invalid ({status!r})")
            elif status == "PROPOSED":
                print(f"    [i] ADR {f.name} is PROPOSED (valid in Phase 2; an arc charter requires ACCEPTED)")
            refs = md_paths(meta.get("justified_by", ""))
            if not refs:
                issues.append(f"ADR {f.name}: no justified_by pointing to a Plan file")
            for ref in refs:
                if not resolve(root, ref, f):
                    issues.append(f"ADR {f.name}: justified_by cites {ref}, which does not exist")
            for ref in md_paths(meta.get("governs", "")):
                if "*" not in ref and not resolve(root, ref, f):
                    issues.append(f"ADR {f.name}: governs {ref}, which does not exist")
    if plan_dir is None:
        issues.append("Missing Plan directory (plan/, Plan/docs/ or Plan/)")

    # Specs
    specs: dict[str, str] = {}
    if specs_dir is None:
        issues.append("Missing specifications directory (spec/ or specs/)")
    else:
        for f in sorted(specs_dir.glob("**/*.md")):
            content = f.read_text(encoding="utf-8")
            specs[f.name] = content
            meta = parse_metadata(content)
            if meta.get("status", "").lower() == "draft" or "status: Draft" in content:
                issues.append(f"Specification {f.name} is still in Draft state (violates living 1:1 parity)")
            gov = md_paths(meta.get("governing_adr", ""))
            for ident in adr_ids(meta.get("governing_adr", "")):
                if not any(name.startswith(ident) for name in adrs):
                    issues.append(f"Specification {f.name}: governing_adr {ident} matches no ADR file")
            if not gov and not adr_ids(meta.get("governing_adr", "")):
                if "ledger" in f.stem.lower():
                    # the enforcement ledger is a register across ADRs (each row names its own ADR), not a governed spec
                    print(f"    [i] {f.name} treated as a register (ledger): no single governing_adr required")
                else:
                    issues.append(f"Specification {f.name}: no governing_adr (a spec without an ADR is hierarchy inversion)")
            for ref in gov:
                if not resolve(root, ref, f):
                    issues.append(f"Specification {f.name}: governing_adr {ref} does not exist")
                elif Path(ref).name in adrs and adrs[Path(ref).name].get("status") in {"REJECTED", "DEPRECATED", "SUPERSEDED"}:
                    issues.append(f"Specification {f.name}: governed by {ref}, whose status is {adrs[Path(ref).name]['status']}")

    # Code
    routes: list[tuple[str, str, str]] = []
    if code_dir is None:
        msg = "No code directory found (code/, poc/ or src/): nothing was examined on the code side"
        if allow_missing_code:
            print(f"    [i] {msg} (allowed by --allow-missing-code)")
        else:
            issues.append(msg)
    else:
        routes = extract_routes(code_dir, issues)
        if not routes:
            print(f"    [i] Code directory {code_dir} has no decorated routes; route parity not examined")
        all_specs_text = "\n".join(specs.values())
        for method, route, filename in routes:
            if route not in all_specs_text:
                issues.append(f"Code route '{method} {route}' in {filename} has no matching specification (unspecified code)")
            else:
                print(f"    [+] OK: {method} {route} named in a specification")

    print("\n--- Verifier Summary ---")
    print(f"    examined: {len(adrs)} ADR(s), {len(specs)} spec(s), {len(routes)} code route(s)"
          f"{'' if code_dir else ' (no code directory)'}")
    if issues:
        print(f"[!] FAILED: {len(issues)} hierarchy integrity issue(s):")
        for issue in issues:
            print(f"    - ❌ {issue}")
        return 1
    print("[+] SUCCESS: no integrity issue found in what was examined (counts above).")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EEEMIAD Hierarchy of Truth Verifier")
    parser.add_argument("--project-root", default=".", help="Root directory of the project")
    parser.add_argument("--allow-missing-code", action="store_true", help="Phase 2: do not fail when no code directory exists yet")
    args = parser.parse_args()
    sys.exit(check_project_hierarchy(args.project_root, args.allow_missing_code))
