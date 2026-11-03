"""Corrida de pruebas del marco de gobierno: alimenta los hooks con casos conocidos y reporta PASS/FAIL.

Uso: python scripts/selftest_governance.py
No toca AWS: solo ejecuta los hooks de .claude/hooks/ con entradas simuladas.
"""
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOOKS = ROOT / ".claude" / "hooks"


def run(hook: str, payload: dict) -> tuple[int, str]:
    r = subprocess.run([sys.executable, str(HOOKS / hook)], input=json.dumps(payload),
                       text=True, capture_output=True)
    return r.returncode, r.stderr.strip()


def bash(cmd: str) -> dict:
    return {"tool_name": "Bash", "tool_input": {"command": cmd}}


def edit(path: pathlib.Path) -> dict:
    return {"tool_name": "Write", "tool_input": {"file_path": str(path)}}


tmp = pathlib.Path(tempfile.mkdtemp())
bad_docker = tmp / "Dockerfile"
bad_docker.write_text("FROM python:latest\nCMD [\"python\"]\n", encoding="utf-8")
bad_k8s_dir = tmp / "k8s"
bad_k8s_dir.mkdir()
bad_k8s = bad_k8s_dir / "deployment.yaml"
bad_k8s.write_text("kind: Deployment\nspec:\n  containers:\n    - image: app:latest\n", encoding="utf-8")

CASES = [
    # (descripcion, hook, payload, exit esperado)
    ("guard_aws: bloquea crear usuario IAM", "guard_aws.py", bash("aws iam create-user --user-name x"), 2),
    ("guard_aws: bloquea comando aws sin profile", "guard_aws.py", bash("aws s3 ls"), 2),
    ("guard_aws: bloquea NAT Gateway (costo)", "guard_aws.py", bash("aws ec2 create-nat-gateway --profile workshop-dev"), 2),
    ("guard_aws: bloquea borrado manual", "guard_aws.py", bash("aws s3 rb s3://x --profile workshop-dev"), 2),
    ("guard_aws: bloquea leer credenciales", "guard_aws.py", bash("cat ~/.aws/credentials"), 2),
    ("guard_aws: permite lectura con profile", "guard_aws.py", bash("aws ecs list-tasks --profile workshop-dev"), 0),
    ("guard_aws: ignora comandos que no son aws", "guard_aws.py", bash("python -m pytest -q"), 0),
    ("lint_infra: rechaza Dockerfile inseguro", "lint_infra.py", edit(bad_docker), 2),
    ("lint_infra: rechaza Deployment sin probes", "lint_infra.py", edit(bad_k8s), 2),
    ("lint_infra: acepta el Dockerfile del repo", "lint_infra.py", edit(ROOT / "Dockerfile"), 0),
    ("lint_infra: acepta k8s/deployment.yaml", "lint_infra.py", edit(ROOT / "k8s" / "deployment.yaml"), 0),
]

failed = 0
for desc, hook, payload, expected in CASES:
    code, err = run(hook, payload)
    ok = code == expected
    failed += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {desc}  (exit {code}, esperado {expected})")
    if err and not ok:
        print("      " + err.replace("\n", "\n      "))
print(f"\n{len(CASES) - failed}/{len(CASES)} casos correctos")
sys.exit(1 if failed else 0)
