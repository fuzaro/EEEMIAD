import subprocess
import sys
import tempfile
from pathlib import Path

from check_falsification import verify_falsification
from verify_hierarchy import check_project_hierarchy, parse_metadata

HERE = Path(__file__).parent
TS = HERE / "typescript"


def _project(root: Path, *, spec_meta: str = "governing_adr: adr/ADR-001-test.md", code: str | None = None,
             adr_status: str = "ACCEPTED", justified: str = "plan/principles.md") -> None:
    (root / "adr").mkdir()
    (root / "spec").mkdir()
    (root / "plan").mkdir()
    (root / "plan" / "principles.md").write_text("# Plan\n", encoding="utf-8")
    (root / "adr" / "ADR-001-test.md").write_text(
        f"# ADR-001\n\n```yaml\nstatus: {adr_status} # comment allowed, as in the template\n"
        f"justified_by: [{justified} §1]\ngoverns: [spec/api.md]\n```\n", encoding="utf-8")
    (root / "spec" / "api.md").write_text(f"# API\n\n```yaml\n{spec_meta}\n```\n\n`GET /v1/health`\n", encoding="utf-8")
    if code is not None:
        (root / "code").mkdir()
        (root / "code" / "app.py").write_text(code, encoding="utf-8")


HEALTH = "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/v1/health')\ndef health(): return {'status': 'ok'}\n"


# ── verify_hierarchy ──────────────────────────────────────────────────────────────────────────

def test_hierarchy_verifier_with_compliant_project():
    with tempfile.TemporaryDirectory() as d:
        _project(Path(d), code=HEALTH)
        assert check_project_hierarchy(d) == 0


def test_hierarchy_verifier_fails_on_unspecified_code():
    with tempfile.TemporaryDirectory() as d:
        _project(Path(d), code="from fastapi import FastAPI\napp = FastAPI()\n@app.post('/v1/admin/backdoor')\ndef b(): pass\n")
        assert check_project_hierarchy(d) == 1


def test_hierarchy_verifier_fails_when_no_code_was_examined():
    """The defect found by validation-by-use: the old verifier reported 100% without reading any code."""
    with tempfile.TemporaryDirectory() as d:
        _project(Path(d), code=None)
        assert check_project_hierarchy(d) == 1
        assert check_project_hierarchy(d, allow_missing_code=True) == 0  # explicit Phase 2 allowance


def test_hierarchy_verifier_fails_on_spec_without_governing_adr():
    with tempfile.TemporaryDirectory() as d:
        _project(Path(d), spec_meta="status: Active", code=HEALTH)
        assert check_project_hierarchy(d) == 1


def test_hierarchy_verifier_fails_on_adr_justified_by_missing_plan():
    with tempfile.TemporaryDirectory() as d:
        _project(Path(d), justified="plan/does-not-exist.md", code=HEALTH)
        assert check_project_hierarchy(d) == 1


def test_hierarchy_verifier_fails_on_invalid_adr_status():
    with tempfile.TemporaryDirectory() as d:
        _project(Path(d), adr_status="APPROVED", code=HEALTH)
        assert check_project_hierarchy(d) == 1


def test_metadata_parser_reads_yaml_fence_and_strips_inline_comments():
    meta = parse_metadata("# T\n\n```yaml\nstatus: ACCEPTED # PROPOSED → ACCEPTED\nratified_by: \"x\"\n```\n")
    assert meta["status"] == "ACCEPTED"
    assert meta["ratified_by"] == "x"


def test_reference_implementation_still_passes():
    assert check_project_hierarchy(str(HERE.parent / "reference-implementation")) == 0


# ── check_falsification ───────────────────────────────────────────────────────────────────────

def _tests(d: str, body: str) -> str:
    t = Path(d) / "tests"
    t.mkdir()
    (t / "test_x.py").write_text(body, encoding="utf-8")
    return str(t)


def test_falsification_verifier_accepts_a_paired_group():
    with tempfile.TemporaryDirectory() as d:
        assert verify_falsification(_tests(d, "def test_auth_valid_token(): pass\ndef test_auth_invalid_token_fails(): pass\n")) == 0


def test_falsification_verifier_fails_on_a_class_without_negative_even_if_the_file_has_one():
    """One negative test in a file no longer vouches for an unrelated group of positives."""
    body = ("def test_login_rejects_bad_password(): pass\n\n"
            "class TestReports:\n    def test_report_renders(self): pass\n    def test_report_has_totals(self): pass\n")
    with tempfile.TemporaryDirectory() as d:
        assert verify_falsification(_tests(d, body)) == 1


def test_falsification_verifier_counts_strict_xfail_as_debt_and_fails_loose_xfail():
    strict = ("import pytest\ndef test_ok(): pass\ndef test_refuses_bad_input(): pass\n"
              "@pytest.mark.xfail(strict=True)\ndef test_future_property(): assert False\n")
    loose = strict.replace("strict=True", "reason='later'")
    with tempfile.TemporaryDirectory() as d:
        assert verify_falsification(_tests(d, strict)) == 0
    with tempfile.TemporaryDirectory() as d:
        assert verify_falsification(_tests(d, loose)) == 1


# ── TypeScript adapter ───────────────────────────────────────────────────────────────────────

def _ts_project(root: Path, *, route_spec: str = "`GET /api/items/{id}`", ledger_flag: str = "ITEMS_MODE") -> None:
    (root / "Plan" / "docs").mkdir(parents=True)
    (root / "Plan" / "decisions").mkdir()
    (root / "specs").mkdir()
    (root / "Plan" / "docs" / "principles.md").write_text("# Plan\n", encoding="utf-8")
    (root / "Plan" / "decisions" / "ADR-001-x.md").write_text("```yaml\nstatus: ACCEPTED\njustified_by: [Plan/docs/principles.md]\n```\n", encoding="utf-8")
    (root / "specs" / "items.md").write_text(f"```yaml\ngoverning_adr: Plan/decisions/ADR-001-x.md\n```\n{route_spec}\n", encoding="utf-8")
    (root / "specs" / "enforcement-ledger.md").write_text(f"| Flag |\n|---|\n| `{ledger_flag}` | off |\n", encoding="utf-8")
    api = root / "app" / "src" / "app" / "api" / "items" / "[id]"
    api.mkdir(parents=True)
    (api / "route.ts").write_text("export async function GET() { return new Response('ok'); }\n", encoding="utf-8")
    (root / "app" / "src" / "server").mkdir(parents=True)
    (root / "app" / "src" / "server" / "flags.ts").write_text("export const F = { ITEMS_MODE: ['off','enforce'] };\n", encoding="utf-8")


def _run(script: str, *args: str) -> int:
    return subprocess.run([sys.executable, str(TS / script), *args], capture_output=True, text=True).returncode


def test_ts_verifier_passes_on_a_coherent_project():
    with tempfile.TemporaryDirectory() as d:
        _ts_project(Path(d))
        assert _run("verify_hierarchy_ts.py", "--project-root", d) == 0


def test_ts_verifier_fails_on_spec_route_without_code_and_on_ledger_flag_mismatch():
    with tempfile.TemporaryDirectory() as d:
        _ts_project(Path(d), route_spec="`GET /api/items/{id}` and `POST /api/items`")
        assert _run("verify_hierarchy_ts.py", "--project-root", d) == 1
    with tempfile.TemporaryDirectory() as d:
        _ts_project(Path(d), ledger_flag="OTHER_MODE")
        assert _run("verify_hierarchy_ts.py", "--project-root", d) == 1


def test_ts_falsification_fails_on_describe_without_negative():
    with tempfile.TemporaryDirectory() as d:
        t = Path(d) / "tests"
        t.mkdir()
        (t / "a.test.ts").write_text('describe("ok", () => {\n  it("works", () => {});\n  it("rejects bad input with 422", () => {});\n});\n'
                                     'describe("lonely", () => {\n  it("renders", () => {});\n});\n', encoding="utf-8")
        assert _run("check_falsification_ts.py", "--test-dir", str(t)) == 1


# ── version and single gate (ch. 08 §8.3) ─────────────────────────────────────────────────────

SCRIPTS = ["verify_hierarchy.py", "check_falsification.py", "typescript/verify_hierarchy_ts.py",
           "typescript/check_falsification_ts.py", "typescript/sweep_ts.py"]


def test_every_harness_script_declares_and_prints_the_same_version():
    import re
    versions = {s: re.search(r'^HARNESS_VERSION = "([^"]+)"', (HERE / s).read_text(encoding="utf-8"), re.M).group(1) for s in SCRIPTS}
    assert len(set(versions.values())) == 1, versions
    out = subprocess.run([sys.executable, str(HERE / "verify_hierarchy.py"), "--project-root", str(HERE.parent / "reference-implementation")],
                         capture_output=True, text=True).stdout
    assert f"EEEMIAD harness {versions['verify_hierarchy.py']}" in out


def _gate(root: str, **env: str) -> subprocess.CompletedProcess:
    import os
    e = {**os.environ, "PYTHON": sys.executable, **env}
    return subprocess.run(["bash", str(HERE / "gate.sh"), root], capture_output=True, text=True, env=e)


def test_gate_approves_a_compliant_project():
    with tempfile.TemporaryDirectory() as d:
        _project(Path(d), code=HEALTH)
        (Path(d) / "tests").mkdir()
        (Path(d) / "tests" / "test_h.py").write_text("def test_health_ok(): pass\ndef test_health_rejects_post(): pass\n", encoding="utf-8")
        r = _gate(d)
        assert r.returncode == 0, r.stdout
        assert "APPROVED" in r.stdout


def test_gate_fails_instead_of_skipping_when_a_required_dependency_is_down_and_counts_failed_steps():
    with tempfile.TemporaryDirectory() as d:
        _project(Path(d), code=HEALTH)
        (Path(d) / "tests").mkdir()
        (Path(d) / "tests" / "test_h.py").write_text("def test_health_ok(): pass\ndef test_health_rejects_post(): pass\n", encoding="utf-8")
        r = _gate(d, GATE_REQUIRE="127.0.0.1:1", GATE_SUITE="exit 3")
        assert r.returncode == 2, r.stdout
        assert "FAIL  dependency 127.0.0.1:1" in r.stdout and "FAIL  test suite" in r.stdout


def test_gate_fails_on_a_project_where_nothing_can_be_examined():
    with tempfile.TemporaryDirectory() as d:
        r = _gate(d)
        assert r.returncode >= 1, r.stdout
