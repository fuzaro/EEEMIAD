"""Tests for starter/eee_init.py: the project it creates, and what it refuses."""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
INIT = HERE / "eee_init.py"


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(INIT), *args, "--yes"], capture_output=True, text=True, stdin=subprocess.DEVNULL)


def _inputs(root: Path) -> Path:
    d = root / "inputs-src"
    (d / "screens").mkdir(parents=True)
    (d / "db.sql").write_text("CREATE TABLE box (id int);\n", encoding="utf-8")
    (d / "screens" / "list.html").write_text("<table></table>\n", encoding="utf-8")
    (d / ".hidden").write_text("x", encoding="utf-8")
    return d


def test_creates_the_governance_tree_kit_gate_and_named_documents():
    with tempfile.TemporaryDirectory() as t:
        dest = Path(t) / "proj"
        r = _run(str(dest), "--name", "Box Archive", "--description", "Tracks boxes.", "--no-git")
        assert r.returncode == 0, r.stdout + r.stderr
        for rel in ["AGENTS.md", "CLAUDE.md", "Plan/docs/pedido.md", "Plan/docs/matriz-pedido-arco.md", "Plan/docs/principios.md",
                    "Plan/decisions/.gitkeep", "specs/charters/.gitkeep", "tests/adversarial/.gitkeep", "eee/log.md",
                    "eee/state/STATE.md", "eee/state/decisions-operator.md", "eee/kit/VERSION", "tools/gate.sh", "tools/gate.env",
                    "tools/eee/verify_hierarchy.py", "tools/eee/typescript/verify_hierarchy_ts.py"]:
            assert (dest / rel).is_file(), rel
        agents = (dest / "AGENTS.md").read_text(encoding="utf-8")
        assert agents.startswith("# AGENTS.md · Box Archive") and "Tracks boxes." in agents
        assert "@AGENTS.md" in (dest / "CLAUDE.md").read_text(encoding="utf-8")
        kit = sorted(p.name for p in (dest / "eee/kit/templates").glob("*.md"))
        assert kit == sorted(p.name for p in (HERE.parent / "templates/pt").glob("*.md"))
        assert re.search(r"^origin: EEEMIAD v\d+\.\d+\.\d+", (dest / "eee/kit/VERSION").read_text(encoding="utf-8"), re.M)


def test_every_path_cited_in_the_generated_agents_md_exists():
    with tempfile.TemporaryDirectory() as t:
        dest = Path(t) / "proj"
        assert _run(str(dest), "--no-git").returncode == 0
        text = (dest / "AGENTS.md").read_text(encoding="utf-8")
        cited = {m for m in re.findall(r"`((?:eee|Plan|specs|tools)/[\w./-]*)`", text)}
        assert cited, "AGENTS.md cites no path"
        missing = [c for c in cited if not (dest / c).exists()]
        assert not missing, missing


def test_journal_entry_one_records_the_real_gate_result():
    with tempfile.TemporaryDirectory() as t:
        dest = Path(t) / "proj"
        assert _run(str(dest), "--no-git").returncode == 0
        row = [l for l in (dest / "eee/log.md").read_text(encoding="utf-8").splitlines() if l.startswith("| 1 |")]
        assert len(row) == 1 and "AAAA-MM-DD" not in row[0]
        assert "FAILED: 1 step(s); esperado na fundação" in row[0]  # no tests yet: R2 fails, and only R2
        gate = subprocess.run(["bash", str(dest / "tools/gate.sh")], capture_output=True, text=True,
                              env={"PATH": "/usr/bin:/bin", "PYTHON": sys.executable})
        assert gate.returncode == 1 and "PASS  hierarchy of truth" in gate.stdout


def test_gate_turns_green_once_a_paired_test_exists():
    with tempfile.TemporaryDirectory() as t:
        dest = Path(t) / "proj"
        assert _run(str(dest), "--no-git").returncode == 0
        (dest / "tests/unit/test_box.py").write_text("def test_box_ok(): pass\ndef test_box_rejects_empty(): pass\n", encoding="utf-8")
        gate = subprocess.run(["bash", str(dest / "tools/gate.sh")], capture_output=True, text=True,
                              env={"PATH": "/usr/bin:/bin", "PYTHON": sys.executable})
        assert gate.returncode == 0, gate.stdout


def test_inputs_are_copied_and_inventoried_with_hidden_files_skipped():
    with tempfile.TemporaryDirectory() as t:
        src = _inputs(Path(t))
        dest = Path(t) / "proj"
        assert _run(str(dest), "--inputs", str(src), "--no-git").returncode == 0
        assert (dest / "Plan/docs/insumos/db.sql").is_file() and (dest / "Plan/docs/insumos/screens/list.html").is_file()
        assert not (dest / "Plan/docs/insumos/.hidden").exists()
        inv = (dest / "Plan/docs/insumos/README.md").read_text(encoding="utf-8")
        assert "`db.sql`" in inv and "`screens/list.html`" in inv and "Nível 1" in inv


def test_private_inputs_are_inventoried_but_never_copied():
    with tempfile.TemporaryDirectory() as t:
        src = _inputs(Path(t))
        dest = Path(t) / "proj"
        assert _run(str(dest), "--inputs", str(src), "--private", "--lang", "en", "--no-git").returncode == 0
        copied = [p for p in (dest / "Plan/docs/inputs").rglob("*") if p.is_file()]
        assert [p.name for p in copied] == ["README.md"]
        assert "CREATE TABLE" not in "".join(p.read_text(encoding="utf-8") for p in dest.rglob("*.md"))
        assert "Private inputs stay out of the repository" in (dest / "AGENTS.md").read_text(encoding="utf-8")
        assert str(src) in (dest / "eee/state/STATE.md").read_text(encoding="utf-8")


def test_refuses_an_existing_eee_project_and_never_overwrites():
    with tempfile.TemporaryDirectory() as t:
        dest = Path(t) / "proj"
        dest.mkdir()
        (dest / "README.md").write_text("mine\n", encoding="utf-8")
        assert _run(str(dest), "--no-git").returncode == 0
        assert (dest / "README.md").read_text(encoding="utf-8") == "mine\n"
        r = _run(str(dest), "--no-git")
        assert r.returncode == 2 and "AGENTS.md" in r.stdout


def test_refuses_missing_inputs_and_a_destination_inside_eeemiad():
    with tempfile.TemporaryDirectory() as t:
        assert _run(str(Path(t) / "p"), "--inputs", str(Path(t) / "nope"), "--no-git").returncode == 2
        assert not (Path(t) / "p").exists()
    assert _run(str(HERE / "tmp-project"), "--no-git").returncode == 2
    assert not (HERE / "tmp-project").exists()


def test_creates_a_git_repository_with_a_first_commit():
    with tempfile.TemporaryDirectory() as t:
        dest = Path(t) / "proj"
        env_cfg = ["-c", "user.name=t", "-c", "user.email=t@example.invalid"]
        r = _run(str(dest))
        assert r.returncode == 0
        log = subprocess.run(["git", *env_cfg, "-C", str(dest), "log", "--oneline"], capture_output=True, text=True)
        status = subprocess.run(["git", "-C", str(dest), "status", "--porcelain"], capture_output=True, text=True).stdout
        if log.returncode == 0:  # commit needs a git identity; without one the files stay staged
            assert "eee_init" in log.stdout and status == ""
        else:
            assert "git commit" in r.stdout
