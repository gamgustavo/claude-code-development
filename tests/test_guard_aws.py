"""Tests del hook .claude/hooks/guard_aws.py (gobierno AWS del curso).

El hook se prueba con entradas simuladas: nunca se ejecuta ningún comando de AWS.
"""
import importlib.util
import io
import json
import os

import pytest

HOOK_PATH = os.path.join(os.path.dirname(__file__), "..", ".claude", "hooks", "guard_aws.py")
_spec = importlib.util.spec_from_file_location("guard_aws", HOOK_PATH)
guard_aws = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(guard_aws)


def run_hook(monkeypatch, command=None, raw=None):
    """Ejecuta main() con el payload de Bash simulado en stdin y devuelve el exit code."""
    payload = raw if raw is not None else json.dumps(
        {"tool_name": "Bash", "tool_input": {"command": command}}
    )
    monkeypatch.setattr("sys.stdin", io.StringIO(payload))
    return guard_aws.main()


@pytest.mark.parametrize(
    "command, fragmento",
    [
        ("aws iam create-user --user-name x --profile workshop-dev", "IAM"),
        ("aws iam attach-role-policy --role-name r --profile workshop-dev", "IAM"),
        ("aws ecs delete-service --cluster c --profile workshop-dev", "borrados"),
        ("aws s3 rm s3://ccd-bucket --recursive --profile workshop-dev", "borrados"),
        ("aws s3 rb s3://ccd-bucket --profile workshop-dev", "borrados"),
        ("aws ec2 run-instances --profile workshop-dev", "costo"),
        ("aws eks create-cluster --profile workshop-dev", "costo"),
        ("aws elbv2 create-load-balancer --profile workshop-dev", "costo"),
        ("cat ~/.aws/credentials", "credenciales"),
        ("cat accessKeys_gustavo.csv", "credenciales"),
        ("aws configure set aws_access_key_id AKIAEXAMPLE", "participante"),
    ],
)
def test_bloquea_comandos_fuera_de_politica(monkeypatch, capsys, command, fragmento):
    assert run_hook(monkeypatch, command) == 2
    assert fragmento in capsys.readouterr().err


def test_bloquea_aws_sin_profile(monkeypatch, capsys):
    assert run_hook(monkeypatch, "aws s3 ls") == 2
    assert "workshop-dev" in capsys.readouterr().err


@pytest.mark.parametrize(
    "command",
    [
        "aws s3 ls --profile workshop-dev",
        "AWS_PROFILE=workshop-dev aws ecs describe-services --cluster ccd-cluster",
        "aws sts get-caller-identity --profile workshop-dev",
        "aws --version",
        "aws help",
    ],
)
def test_permite_comandos_de_solo_lectura(monkeypatch, command):
    assert run_hook(monkeypatch, command) == 0


@pytest.mark.parametrize("command", ["ls -la", "python -m pytest -q", "git status", ""])
def test_ignora_comandos_que_no_son_de_aws(monkeypatch, command):
    assert run_hook(monkeypatch, command) == 0


def test_entrada_json_invalida_no_bloquea(monkeypatch):
    assert run_hook(monkeypatch, raw="esto no es json") == 0


def test_payload_sin_comando_no_bloquea(monkeypatch):
    assert run_hook(monkeypatch, raw=json.dumps({"tool_name": "Bash"})) == 0
