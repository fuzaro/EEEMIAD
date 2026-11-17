#!/usr/bin/env bash
# EEEMIAD single gate (ch. 08 §8.3). One command, one exit code, for any person, agent or harness.
# Copy it into the project (e.g. tools/gate.sh), keep HARNESS_VERSION of the copied verifiers declared,
# and add the project's own steps at the marked place. It must fail, never skip, when a dependency is missing.
#
# Usage: gate.sh [project-root]      (default: .)
# Environment:
#   PYTHON         interpreter to use (default: first python >= 3.8 found)
#   TEST_DIR       tests directory, relative to the root (default: tests)
#   HARNESS_DIR    where verify_hierarchy.py and check_falsification.py live (default: this script's directory)
#   GATE_ARGS      extra arguments for verify_hierarchy.py (e.g. --allow-missing-code in Phase 2)
#   GATE_REQUIRE   space-separated host:port that must accept connections (e.g. a test database)
#   GATE_SUITE     the project's test-suite command, run with bash -c from the root
# Exit: number of failed steps (0 = approved); 98 = no suitable Python.
set -u
HARNESS_DIR=${HARNESS_DIR:-$(cd "$(dirname "$0")" && pwd)}
ROOT=${1:-.}
TEST_DIR=${TEST_DIR:-tests}
cd "$ROOT" || exit 99

find_python() {
  for c in "${PYTHON:-}" python3.13 python3.12 python3.11 python3.10 python3.9 python3.8 python3; do
    [ -n "$c" ] || continue
    command -v "$c" >/dev/null 2>&1 || continue
    "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' 2>/dev/null && { echo "$c"; return 0; }
  done
  return 1
}
PY=$(find_python) || { echo "[gate] no Python >= 3.8 found; set PYTHON=<path>"; exit 98; }

FAILED=0
RESULTS=""
step() {  # step <name> <command...>
  local name=$1; shift
  echo; echo "=== [gate] $name"
  if "$@"; then RESULTS="$RESULTS\n  PASS  $name"; else RESULTS="$RESULTS\n  FAIL  $name (exit $?)"; FAILED=$((FAILED + 1)); fi
}
reachable() {  # reachable host:port — a missing dependency fails the gate instead of skipping tests
  local host=${1%:*} port=${1##*:}
  (exec 3<>"/dev/tcp/$host/$port") 2>/dev/null || { echo "$1 does not accept connections"; return 1; }
}

# shellcheck disable=SC2086
step "hierarchy of truth" "$PY" "$HARNESS_DIR/verify_hierarchy.py" --project-root . ${GATE_ARGS:-}
step "disagreeable pairs (R2)" "$PY" "$HARNESS_DIR/check_falsification.py" --test-dir "$TEST_DIR"
for dep in ${GATE_REQUIRE:-}; do step "dependency $dep" reachable "$dep"; done
[ -n "${GATE_SUITE:-}" ] && step "test suite" bash -c "$GATE_SUITE"
# ── project steps go here (Phase 8 sweep, DDL = spec, adapter checks, ...) ──

echo; echo "=== [gate] summary"; printf "%b\n" "$RESULTS"
if [ "$FAILED" -gt 0 ]; then echo "[gate] FAILED: $FAILED step(s)"; else echo "[gate] APPROVED"; fi
exit "$FAILED"
