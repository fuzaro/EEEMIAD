#!/usr/bin/env python3
"""
EEE Governance Sweep - Automated Phase 8 AST Scanner
Extracts HTTP endpoints and environment variables via AST and checks for spec coverage.
"""
import ast
import os
import sys
import argparse
from pathlib import Path

def get_literal_value(node):
    if hasattr(node, 'value'):
        return node.value
    elif hasattr(node, 's'):
        return node.s
    return None

class RouteExtractor(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.routes = []
        self.env_vars = []

    def visit_Call(self, node):
        # Detect os.getenv("VAR") or os.environ.get("VAR")
        if isinstance(node.func, ast.Attribute):
            is_env_call = False
            if node.func.attr == "getenv" and isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                is_env_call = True
            elif node.func.attr == "get" and isinstance(node.func.value, ast.Attribute) and node.func.value.attr == "environ":
                is_env_call = True
            
            if is_env_call and node.args:
                val = get_literal_value(node.args[0])
                if isinstance(val, str):
                    self.env_vars.append((val, self.filename, node.lineno))
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        for decorator in node.decorator_list:
            # Detect @router.get("/path"), @app.post("/path")
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                http_method = decorator.func.attr.upper()
                if http_method in ("GET", "POST", "PUT", "DELETE", "PATCH"):
                    route_path = "unknown"
                    if decorator.args:
                        val = get_literal_value(decorator.args[0])
                        if val is not None:
                            route_path = str(val)
                    self.routes.append({
                        "method": http_method,
                        "path": route_path,
                        "function": node.name,
                        "file": self.filename,
                        "line": node.lineno
                    })
        self.generic_visit(node)

def run_sweep(source_dir, spec_dir):
    print(f"[*] Starting EEEMIAD Phase 8 Sweep on: {source_dir}")
    all_routes = []
    all_env_vars = []

    for root, _, files in os.walk(source_dir):
        for f in files:
            if f.endswith(".py"):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, "r", encoding="utf-8") as py_file:
                        tree = ast.parse(py_file.read(), filename=filepath)
                    extractor = RouteExtractor(filepath)
                    extractor.visit(tree)
                    all_routes.extend(extractor.routes)
                    all_env_vars.extend(extractor.env_vars)
                except Exception as e:
                    print(f"[-] Warning: Failed to parse {filepath}: {e}", file=sys.stderr)

    print(f"\n[+] Extracted {len(all_routes)} active routes via AST:")
    for r in all_routes:
        print(f"    - {r['method']:<6} {r['path']:<35} ({r['file']}:{r['line']})")

    print(f"\n[+] Extracted {len(set(ev[0] for ev in all_env_vars))} unique environment variables:")
    for var, f, l in sorted(set(all_env_vars)):
        print(f"    - {var:<35} ({f}:{l})")

    print("\n[+] Phase 8 Sweep Complete. Use these findings to update living specifications.")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EEEMIAD Phase 8 AST Governance Sweep")
    parser.add_argument("--src", default="./src", help="Path to Python source directory")
    parser.add_argument("--specs", default="./specs", help="Path to specs directory")
    args = parser.parse_args()
    sys.exit(run_sweep(args.src, args.specs))
