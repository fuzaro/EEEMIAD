import pytest
import tempfile
from pathlib import Path
from verify_hierarchy import check_project_hierarchy
from check_falsification import verify_falsification

def test_hierarchy_verifier_with_mock_compliant_project():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        (root / "adr").mkdir()
        (root / "spec").mkdir()
        (root / "code").mkdir()

        # 1. ADR
        adr_file = root / "adr" / "ADR-001-test.md"
        adr_file.write_text("---\nstatus: ACCEPTED\n---\n# ADR-001\nGoverns specs/api.md", encoding="utf-8")

        # 2. Spec
        spec_file = root / "spec" / "api.md"
        spec_file.write_text("# API Spec\nEndpoint: `/v1/health`\nMethod: GET", encoding="utf-8")

        # 3. Code matching Spec
        code_file = root / "code" / "app.py"
        code_file.write_text(
            "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/v1/health')\ndef health(): return {'status': 'ok'}",
            encoding="utf-8"
        )

        exit_code = check_project_hierarchy(str(root))
        assert exit_code == 0

def test_hierarchy_verifier_fails_on_unspecified_code():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        (root / "adr").mkdir()
        (root / "spec").mkdir()
        (root / "code").mkdir()

        # Spec
        (root / "spec" / "api.md").write_text("# API Spec\nEndpoint: `/v1/health`", encoding="utf-8")

        # Code introducing an unratified ghost endpoint
        (root / "code" / "app.py").write_text(
            "from fastapi import FastAPI\napp = FastAPI()\n@app.post('/v1/admin/unspecified_backdoor')\ndef backdoor(): pass",
            encoding="utf-8"
        )

        exit_code = check_project_hierarchy(str(root))
        assert exit_code == 1

def test_falsification_verifier():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / "tests"
        test_dir.mkdir()

        # Valid balanced test file
        test_file = test_dir / "test_auth.py"
        test_file.write_text(
            "def test_auth_valid_token(): pass\ndef test_auth_invalid_token_fails(): pass\n",
            encoding="utf-8"
        )

        exit_code = verify_falsification(str(test_dir))
        assert exit_code == 0
