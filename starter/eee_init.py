#!/usr/bin/env python3
"""
eee_init · creates a new project ready for EEE (EEEMIAD ch. 08 §1 step 1, §8).

    python3 starter/eee_init.py <destination> [options]

What it does, without asking you to copy anything by hand:
  1. creates the governance tree (Plan/, specs/, tests/, eee/, tools/);
  2. copies the EEEMIAD templates into eee/kit/ and records origin and version (eee/kit/VERSION);
  3. copies the verifiers and the single gate into tools/ (tools/gate.sh + tools/gate.env);
  4. creates AGENTS.md (entry point for people and agents), CLAUDE.md (thin adapter), the request,
     the request × arc matrix, the one-page Plan, the operational state, the operator decisions and
     the evidence journal, already named after the project;
  5. registers your inputs (database layout, screens, UX template...): copied into Plan/docs/inputs
     (insumos/ in Portuguese), or, with --private, left where they are and only inventoried (name, size, hash);
  6. runs the gate once and records the result as entry #1 of the journal;
  7. creates the git repository and the first commit (unless --no-git).

It never overwrites an existing file and refuses a destination that already has an AGENTS.md.
Requires Python >= 3.8; the gate also needs bash (Linux, macOS, WSL or Git Bash on Windows).
Exit: 0 ok · 2 refused (invalid destination or inputs) · 3 Python too old.
"""

import argparse
import datetime as dt
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

if sys.version_info < (3, 8):
    sys.stderr.write("eee_init: Python >= 3.8 required\n")
    sys.exit(3)

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
HARNESS = REPO / "examples" / "verification-harness"
HARNESS_FILES = ["verify_hierarchy.py", "check_falsification.py", "gate.sh",
                 "typescript/verify_hierarchy_ts.py", "typescript/check_falsification_ts.py",
                 "typescript/sweep_ts.py", "typescript/README.md"]

# Per-language file names and texts. Templates hold the content; these are only the glue.
L = {
    "pt": {
        "request": "pedido.md", "matrix": "matriz-pedido-arco.md", "plan": "principios.md", "inputs": "insumos",
        "project": "[Projeto]", "date_ph": "AAAA-MM-DD",
        "desc_ph": "[Uma frase sobre o sistema e a stack.]",
        "private_ph": "1. [Dados privados: o que nunca entra no repositório.]",
        "private_rule": "1. **Insumos privados ficam fora do repositório** (onde estão: `eee/state/STATE.md`, seção Insumos). Nenhum valor deles entra aqui; use só a forma para gerar dados de teste.",
        "ask_name": "Nome do projeto", "ask_desc": "Uma frase: o que o sistema faz e para quem (Enter para depois)",
        "ask_inputs": "Diretório dos insumos (layout de banco, telas, UX...; Enter se não houver)",
        "ask_private": "Os insumos têm dados reais ou privados? [s/N]", "yes": ("s", "sim", "y", "yes"),
        "refuse_agents": "recusado: {d} já tem AGENTS.md (já é um projeto EEE)",
        "refuse_inputs": "recusado: diretório de insumos não existe: {d}",
        "refuse_inside": "recusado: o destino não pode ficar dentro do EEEMIAD; escolha outra pasta",
        "skip": "  já existe, mantido: {p}",
        "inputs_title": "# 📥 Insumos · {name}",
        "inputs_intro": ("Material de entrada do projeto (EEEMIAD ch. 04 Fase 1). **Nível 1 (R15): é documento, não verdade.** "
                         "Toda afirmação tirada daqui vai com o nível; contradição com o pedido vai para a fase de perguntas.\n\n"
                         "**Somente leitura.** Não edite estes arquivos: versão nova = arquivo novo + linha no diário (`eee/log.md`)."),
        "inputs_private": ("**Privados: não estão no repositório.** Origem registrada em `eee/state/STATE.md`. "
                           "O inventário abaixo (nome, tamanho, hash) permite ver se mudaram."),
        "inputs_head": "| Arquivo | Bytes | sha256 (12) |",
        "state_inputs": "## Insumos\n\n| Onde | Copiados para o repo? | Inventário |\n|---|---|---|\n| {where} | {copied} | `Plan/docs/{dir}/README.md` |\n\n",
        "copied_yes": "sim", "copied_no": "**não** (privados)",
        "state_phase_note": "> **Fase de fundação.** Siga as pendências em ordem. Não escreva código antes do Plan aprovado e da ADR-001 aceita.\n\n",
        "pending": [
            ("Colar o pedido, literalmente, em `Plan/docs/pedido.md` §1", "quem pede"),
            ("Responder à fase de perguntas (`pedido.md` §2); o agente pode perguntar e anotar", "quem decide"),
            ("Ler os insumos e registrar contradições com o pedido como perguntas", "agente + quem decide"),
            ("Escrever `Plan/docs/principios.md` (uma página) e aprová-lo", "quem decide aprova"),
            ("Quebrar o pedido em itens na `Plan/docs/matriz-pedido-arco.md`", "agente; quem decide revisa"),
            ("ADR-001 (arquitetura) em `Plan/decisions/`, a partir de `eee/kit/templates/adr-template.md`; nasce PROPOSED", "quem decide ratifica"),
            ("Specs com M11 em `specs/` (layout de banco → DDL; telas → spec de telas)", "agente"),
            ("Primeiro charter em `specs/charters/` (template de charter, com `request_item`)", "quem decide abre"),
            ("Ajustar `tools/gate.env` quando o primeiro código e o primeiro teste existirem", "agente"),
        ],
        "log_row": ("| 1 | {date} | fundação | ch. 08 §1 passo 1; §8 | Projeto criado com `starter/eee_init.py` (EEEMIAD {ver}, {commit}): "
                    "árvore de governança, kit de templates, gate único, AGENTS.md, pedido, matriz, Plan, estado. Insumos: {inputs} "
                    "| `tools/gate.sh` → {gate} (nível 1) | **ok** |"),
        "gate_expected": "esperado na fundação: sem testes ainda, o passo R2 reprova até o primeiro teste",
        "inputs_none": "nenhum", "inputs_copied": "{n} arquivo(s) copiados para `Plan/docs/insumos/`",
        "inputs_priv": "{n} arquivo(s) privados, inventariados e fora do repo",
        "claude": "@AGENTS.md\n\nAdaptador do Claude Code. O conteúdo canônico está em `AGENTS.md` e `eee/`; não acrescente regras aqui.\n",
        "playbooks": ("# Playbooks\n\nProcedimentos por papel, sem nome de ferramenta ou modelo (EEEMIAD ch. 08 §8.2). "
                      "Opcional: para trabalhar com dois agentes ou com divisão de tarefas, instale os playbooks do "
                      "EEEMIAD-dual (`docs/pt/04-instalacao-neutra.md`). Sem eles, siga o EEEMIAD ch. 08.\n"),
        "readme": "# {name}\n\n{desc}\n\nComece por [AGENTS.md](AGENTS.md). Verificação: `tools/gate.sh`.\n",
        "gate_env": """# Configuração do gate único (EEEMIAD ch. 08 §8.3). Edite conforme o projeto cresce.
# py = Python (verificadores por AST) · ts = Next.js/TypeScript (ver tools/eee/typescript/README.md)
HARNESS_LANG={lang}
TEST_DIR=tests
# Fase de fundação: ainda não há código. Remova --allow-missing-code quando o primeiro código existir.
# Em ts, acrescente --api-root e --flags-file conforme o projeto.
GATE_ARGS="--allow-missing-code"
# Dependências que precisam estar no ar (host:porta separados por espaço), ex.: banco de teste "127.0.0.1:5432"
GATE_REQUIRE=""
# Comando da suíte de testes, ex.: "pytest -q tests" ou "npm test"
GATE_SUITE=""
""",
        "done": "Projeto criado em {d}",
        "next": """
Próximos passos (também em eee/state/STATE.md, seção Pendências):
  1. Abra Plan/docs/pedido.md e cole o pedido, com as suas palavras.
  2. Abra um agente de código (Claude Code, Codex, Cursor...) na pasta do projeto e cole:

     Leia o AGENTS.md e o eee/state/STATE.md. Estamos na fase de fundação da EEE.
     Faça comigo a fase de perguntas do Plan/docs/pedido.md, uma pergunta por vez,
     e anote as respostas. Depois leia os insumos, escreva o Plan/docs/principios.md
     e a matriz pedido × arco, e pare para eu aprovar. Não escreva código.

  3. Guia completo: EEEMIAD docs/pt/12-primeiros-passos.md
""",
    },
    "en": {
        "request": "request.md", "matrix": "request-matrix.md", "plan": "principles.md", "inputs": "inputs",
        "project": "[Project]", "date_ph": "YYYY-MM-DD",
        "desc_ph": "[One sentence about the system and the stack.]",
        "private_ph": "1. [Private data: what never enters the repository.]",
        "private_rule": "1. **Private inputs stay out of the repository** (where they are: `eee/state/STATE.md`, Inputs section). None of their values enters here; use only their shape to generate test data.",
        "ask_name": "Project name", "ask_desc": "One sentence: what the system does and for whom (Enter to skip)",
        "ask_inputs": "Inputs directory (database layout, screens, UX...; Enter if none)",
        "ask_private": "Do the inputs hold real or private data? [y/N]", "yes": ("y", "yes"),
        "refuse_agents": "refused: {d} already has an AGENTS.md (it is already an EEE project)",
        "refuse_inputs": "refused: inputs directory does not exist: {d}",
        "refuse_inside": "refused: the destination cannot be inside EEEMIAD; choose another folder",
        "skip": "  already exists, kept: {p}",
        "inputs_title": "# 📥 Inputs · {name}",
        "inputs_intro": ("Input material of the project (EEEMIAD ch. 04 Phase 1). **Level 1 (R15): a document, not truth.** "
                         "Every claim taken from here carries its level; a contradiction with the request goes to the question phase.\n\n"
                         "**Read-only.** Do not edit these files: a new version = a new file + a journal row (`eee/log.md`)."),
        "inputs_private": ("**Private: not in the repository.** Origin recorded in `eee/state/STATE.md`. "
                           "The inventory below (name, size, hash) shows whether they changed."),
        "inputs_head": "| File | Bytes | sha256 (12) |",
        "state_inputs": "## Inputs\n\n| Where | Copied into the repo? | Inventory |\n|---|---|---|\n| {where} | {copied} | `Plan/docs/{dir}/README.md` |\n\n",
        "copied_yes": "yes", "copied_no": "**no** (private)",
        "state_phase_note": "> **Foundation phase.** Follow the pending items in order. Write no code before the Plan is approved and ADR-001 accepted.\n\n",
        "pending": [
            ("Paste the request, verbatim, into `Plan/docs/request.md` §1", "requester"),
            ("Answer the question phase (`request.md` §2); the agent can ask and record", "who decides"),
            ("Read the inputs and record contradictions with the request as questions", "agent + who decides"),
            ("Write `Plan/docs/principles.md` (one page) and approve it", "who decides approves"),
            ("Break the request into items in `Plan/docs/request-matrix.md`", "agent; who decides reviews"),
            ("ADR-001 (architecture) in `Plan/decisions/`, from `eee/kit/templates/adr-template.md`; born PROPOSED", "who decides ratifies"),
            ("Specs with M11 in `specs/` (database layout → DDL; screens → screens spec)", "agent"),
            ("First charter in `specs/charters/` (charter template, with `request_item`)", "who decides opens"),
            ("Adjust `tools/gate.env` once the first code and the first test exist", "agent"),
        ],
        "log_row": ("| 1 | {date} | foundation | ch. 08 §1 step 1; §8 | Project created with `starter/eee_init.py` (EEEMIAD {ver}, {commit}): "
                    "governance tree, template kit, single gate, AGENTS.md, request, matrix, Plan, state. Inputs: {inputs} "
                    "| `tools/gate.sh` → {gate} (level 1) | **ok** |"),
        "gate_expected": "expected at foundation: with no tests yet, the R2 step fails until the first test",
        "inputs_none": "none", "inputs_copied": "{n} file(s) copied into `Plan/docs/inputs/`",
        "inputs_priv": "{n} private file(s), inventoried and kept out of the repo",
        "claude": "@AGENTS.md\n\nClaude Code adapter. The canonical content is in `AGENTS.md` and `eee/`; do not add rules here.\n",
        "playbooks": ("# Playbooks\n\nRole procedures, with no tool or model name (EEEMIAD ch. 08 §8.2). "
                      "Optional: to work with two agents or with task division, install the EEEMIAD-dual playbooks "
                      "(`docs/en/04-harness-neutral-installation.md`). Without them, follow EEEMIAD ch. 08.\n"),
        "readme": "# {name}\n\n{desc}\n\nStart with [AGENTS.md](AGENTS.md). Verification: `tools/gate.sh`.\n",
        "gate_env": """# Single gate configuration (EEEMIAD ch. 08 §8.3). Edit it as the project grows.
# py = Python (AST verifiers) · ts = Next.js/TypeScript (see tools/eee/typescript/README.md)
HARNESS_LANG={lang}
TEST_DIR=tests
# Foundation phase: no code yet. Remove --allow-missing-code once the first code exists.
# With ts, add --api-root and --flags-file as the project needs.
GATE_ARGS="--allow-missing-code"
# Dependencies that must be up (space-separated host:port), e.g. a test database "127.0.0.1:5432"
GATE_REQUIRE=""
# Test-suite command, e.g. "pytest -q tests" or "npm test"
GATE_SUITE=""
""",
        "done": "Project created at {d}",
        "next": """
Next steps (also in eee/state/STATE.md, Pending section):
  1. Open Plan/docs/request.md and paste the request, in your own words.
  2. Open a coding agent (Claude Code, Codex, Cursor...) in the project folder and paste:

     Read AGENTS.md and eee/state/STATE.md. We are in the EEE foundation phase.
     Run the question phase of Plan/docs/request.md with me, one question at a time,
     and record the answers. Then read the inputs, write Plan/docs/principles.md
     and the request × arc matrix, and stop for my approval. Do not write code.

  3. Full guide: EEEMIAD docs/en/12-getting-started.md
""",
    },
}

GITIGNORE = "scratch/\n__pycache__/\n*.pyc\n.venv/\nnode_modules/\n.env\n.env.*\n"
GATE_WRAPPER = """#!/usr/bin/env bash
# Single gate of the project: one command, one exit code (EEEMIAD ch. 08 §8.3).
# Configuration: tools/gate.env. Verifiers copied from EEEMIAD: tools/eee/ (origin in eee/kit/VERSION).
cd "$(dirname "$0")/.." || exit 99
set -a; . tools/gate.env; set +a
exec bash tools/eee/gate.sh .
"""


class Init:
    def __init__(self, dest: Path, lang: str):
        self.dest, self.t, self.lang = dest, L[lang], lang
        self.created = []  # type: list

    def write(self, rel: str, text: str, executable: bool = False) -> None:
        p = self.dest / rel
        if p.exists():
            print(self.t["skip"].format(p=rel))
            return
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        if executable:
            p.chmod(0o755)
        self.created.append(rel)

    def copy(self, src: Path, rel: str) -> None:
        p = self.dest / rel
        if p.exists():
            print(self.t["skip"].format(p=rel))
            return
        p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, p)
        self.created.append(rel)

    def template(self, name: str) -> str:
        return (REPO / "templates" / self.lang / name).read_text(encoding="utf-8")


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def eeemiad_version():  # -> (version, commit)
    m = re.search(r"^## \[(\d+\.\d+\.\d+)\]", (REPO / "CHANGELOG.md").read_text(encoding="utf-8"), re.M)
    ver = "v" + m.group(1) if m else "v?"
    try:
        commit = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                                capture_output=True, text=True, check=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain", "--", "templates", "examples", "starter"],
                               capture_output=True, text=True).stdout.strip()
        commit += " +local changes" if dirty else ""
    except (OSError, subprocess.CalledProcessError):
        commit = "commit unknown (not a git clone)"
    return ver, commit


def list_inputs(src: Path):
    return sorted(f for f in src.rglob("*") if f.is_file()
                  and not any(part.startswith(".") for part in f.relative_to(src).parts))


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        ans = input(f"{prompt}{suffix}: ").strip()
    except EOFError:
        ans = ""
    return ans or default


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Create a new project ready for EEE (EEEMIAD ch. 08 §1, §8).")
    ap.add_argument("destino", metavar="destination", help="project folder (created if missing)")
    ap.add_argument("--nome", "--name", dest="name", help="project name (default: folder name)")
    ap.add_argument("--descricao", "--description", dest="desc", default=None, help="one sentence about the system")
    ap.add_argument("--insumos", "--inputs", dest="inputs", default=None, help="folder with the project inputs")
    ap.add_argument("--privado", "--private", dest="private", action="store_true",
                    help="inputs hold real/private data: inventory them, do not copy them")
    ap.add_argument("--idioma", "--lang", dest="lang", choices=["pt", "en"], default="pt")
    ap.add_argument("--stack", choices=["py", "ts"], default="py", help="verifier flavour: py or ts (Next.js/TypeScript)")
    ap.add_argument("--sem-git", "--no-git", dest="no_git", action="store_true")
    ap.add_argument("--sim", "--yes", dest="yes", action="store_true", help="never ask; use defaults")
    a = ap.parse_args(argv)
    t = L[a.lang]

    dest = Path(a.destino).expanduser().resolve()
    if dest == REPO or REPO in dest.parents:
        print(t["refuse_inside"]); return 2
    if (dest / "AGENTS.md").exists():
        print(t["refuse_agents"].format(d=dest)); return 2

    interactive = sys.stdin.isatty() and not a.yes
    name = a.name or (ask(t["ask_name"], dest.name) if interactive else dest.name)
    desc = a.desc if a.desc is not None else (ask(t["ask_desc"]) if interactive else "")
    inputs = a.inputs if a.inputs is not None else (ask(t["ask_inputs"]) if interactive else "")
    private = a.private
    if inputs and not a.private and interactive:
        private = ask(t["ask_private"]).lower() in t["yes"]
    src_inputs = Path(inputs).expanduser().resolve() if inputs else None
    if src_inputs and not src_inputs.is_dir():
        print(t["refuse_inputs"].format(d=src_inputs)); return 2

    today = dt.date.today().isoformat()
    ver, commit = eeemiad_version()
    it = Init(dest, a.lang)
    dest.mkdir(parents=True, exist_ok=True)

    # 1. governance tree (empty folders get a .gitkeep so git keeps them)
    for d in ["Plan/decisions", "specs/charters", "tests/unit", "tests/integration", "tests/adversarial"]:
        it.write(f"{d}/.gitkeep", "")
    (dest / "scratch").mkdir(exist_ok=True)

    # 2. template kit with origin and version
    kit = sorted((REPO / "templates" / a.lang).glob("*.md"))
    for f in kit:
        it.copy(f, f"eee/kit/templates/{f.name}")
    lines = [f"origin: EEEMIAD {ver} ({commit})", f"copied_on: {today}", f"language: {a.lang}", "files:"]
    lines += [f"  templates/{a.lang}/{f.name}  sha256:{sha(f)[:12]}" for f in kit]
    lines += [f"  examples/verification-harness/{h}  sha256:{sha(HARNESS / h)[:12]}" for h in HARNESS_FILES]
    it.write("eee/kit/VERSION", "\n".join(lines) + "\n")

    # 3. verifiers and single gate
    for h in HARNESS_FILES:
        it.copy(HARNESS / h, f"tools/eee/{h}")
    it.write("tools/gate.sh", GATE_WRAPPER, executable=True)
    it.write("tools/gate.env", t["gate_env"].format(lang=a.stack))

    # 5. inputs (before the documents, so the state can point to them)
    n_inputs, inputs_note = 0, t["inputs_none"]
    if src_inputs:
        files = list_inputs(src_inputs)
        n_inputs = len(files)
        rows = []
        for f in files:
            rel = f.relative_to(src_inputs).as_posix()
            if not private:
                it.copy(f, f"Plan/docs/{t['inputs']}/{rel}")
            rows.append(f"| `{rel}` | {f.stat().st_size} | `{sha(f)[:12]}` |")
        body = [t["inputs_title"].format(name=name), "", t["inputs_intro"], ""]
        if private:
            body += [t["inputs_private"], ""]
        body += [t["inputs_head"], "|---|---|---|", *rows, ""]
        it.write(f"Plan/docs/{t['inputs']}/README.md", "\n".join(body))
        inputs_note = (t["inputs_priv"] if private else t["inputs_copied"]).format(n=n_inputs)

    # 4. documents named after the project
    def fill(text: str) -> str:
        return text.replace(t["project"], name)

    agents = fill(it.template("agents-entry-template.md"))
    if desc:
        agents = agents.replace(t["desc_ph"], desc)
    if src_inputs and private:
        agents = agents.replace(t["private_ph"], t["private_rule"])
    it.write("AGENTS.md", agents)
    it.write("CLAUDE.md", t["claude"])
    it.write("README.md", t["readme"].format(name=name, desc=desc or t["desc_ph"]))
    it.write(".gitignore", GITIGNORE)
    it.write("eee/playbooks/README.md", t["playbooks"])
    it.write(f"Plan/docs/{t['request']}", fill(it.template("request-template.md")).replace(t["date_ph"], today, 1))
    it.write(f"Plan/docs/{t['matrix']}", fill(it.template("request-matrix-template.md")).replace(t["date_ph"], today, 1))
    it.write(f"Plan/docs/{t['plan']}", fill(it.template("foundational-plan-template.md")))
    it.write("eee/state/decisions-operator.md", fill(it.template("operator-decisions-template.md")))

    state = fill(it.template("operational-state-template.md")).replace(t["date_ph"], today, 1)
    pend_head = "## Pendências" if a.lang == "pt" else "## Pending"
    before, _, _ = state.partition(pend_head)
    if src_inputs:
        where = f"`{src_inputs}`" if private else f"`Plan/docs/{t['inputs']}/`"
        before += t["state_inputs"].format(where=where, copied=t["copied_no"] if private else t["copied_yes"], dir=t["inputs"])
    head = "| # | O que | Bloqueio / quem decide |" if a.lang == "pt" else "| # | What | Blocker / who decides |"
    rows = "\n".join(f"| {i} | {w} | {who} |" for i, (w, who) in enumerate(t["pending"], 1))
    state = before + pend_head + "\n\n" + t["state_phase_note"] + head + "\n|---|---|---|\n" + rows + "\n"
    it.write("eee/state/STATE.md", state)

    # 6. run the gate once and record the result honestly in journal entry #1
    gate_result = "not run (bash not found)" if a.lang == "en" else "não executado (bash ausente)"
    if shutil.which("bash"):
        env = {**os.environ, "PYTHON": sys.executable}
        r = subprocess.run(["bash", str(dest / "tools/gate.sh")], capture_output=True, text=True, env=env)
        print(r.stdout[-1500:])
        verdict = "APPROVED" if r.returncode == 0 else f"FAILED: {r.returncode} step(s)"
        only_r2_without_tests = (r.returncode == 1 and "FAIL  disagreeable pairs (R2)" in r.stdout
                                 and re.search(r"No tests found|no \*\.test", r.stdout) is not None)
        gate_result = f"{verdict}; {t['gate_expected']}" if only_r2_without_tests else verdict
    journal = fill(it.template("evidence-journal-template.md"))
    journal = re.sub(r"^\| 1 \| (AAAA|YYYY)-MM-DD .*\n\| 2 \| .*\n",
                     t["log_row"].format(date=today, ver=ver, commit=commit, inputs=inputs_note, gate=gate_result) + "\n",
                     journal, count=1, flags=re.M)
    it.write("eee/log.md", journal)

    # 7. git
    if not a.no_git and shutil.which("git") and not (dest / ".git").exists():
        subprocess.run(["git", "init", "-q"], cwd=dest)
        subprocess.run(["git", "add", "-A"], cwd=dest)
        msg = f"EEE: projeto criado com eee_init (EEEMIAD {ver})" if a.lang == "pt" else f"EEE: project created with eee_init (EEEMIAD {ver})"
        c = subprocess.run(["git", "commit", "-q", "-m", msg], cwd=dest, capture_output=True, text=True)
        if c.returncode:
            print(("git: arquivos preparados, mas o commit falhou (configure user.name e user.email e rode git commit):\n"
                   if a.lang == "pt" else "git: files staged, but the commit failed (set user.name and user.email, then run git commit):\n")
                  + c.stderr.strip())

    print(t["done"].format(d=dest) + f" · {len(it.created)} file(s) · EEEMIAD {ver} ({commit})")
    print(t["next"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
