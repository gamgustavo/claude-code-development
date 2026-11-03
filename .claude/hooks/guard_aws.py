#!/usr/bin/env python
"""Hook PreToolUse (Bash) — guardia de gobierno AWS del curso.

stdin: {"tool_name": "Bash", "tool_input": {"command": "..."}}
exit 0 permite; exit 2 bloquea y devuelve stderr a Claude.
"""
import json
import re
import sys

RULES = [
    (r"\baws\s+iam\s+(create|delete|put|attach|detach|update)",
     "Política: Claude no modifica IAM. Los roles viven en infra/*.yml."),
    (r"\baws\s+\S+\s+delete-|\baws\s+s3\s+(rb|rm)\b|\baws\s+ecr\s+batch-delete",
     "Política: borrados manuales no permitidos. Usa infra/destroy.sh o el pipeline."),
    (r"\baws\s+(ec2\s+(run-instances|create-nat-gateway)|eks\s+create|elbv2\s+create-load-balancer|rds\s+create)",
     "Política de costo: sin EC2, NAT, EKS, ALB ni RDS en este demo (ver standards/aws.md)."),
    (r"(~|\$HOME|/)\.aws/credentials|accessKeys.*\.csv",
     "Política: no se leen ni imprimen credenciales."),
    (r"\baws\s+configure\s+(set|import)|\baws\s+configure\b.*aws_secret",
     "Política: las credenciales las configura el participante, no Claude."),
]


def main() -> int:
    try:
        cmd = (json.load(sys.stdin).get("tool_input") or {}).get("command", "")
    except json.JSONDecodeError:
        return 0
    if not re.search(r"\baws\b|\.aws|accessKeys", cmd):
        return 0
    for pattern, msg in RULES:
        if re.search(pattern, cmd, re.I):
            print(f"BLOQUEADO por guard_aws.py: {msg}", file=sys.stderr)
            return 2
    if re.search(r"\baws\s+(?!configure|--version|help)", cmd) and "workshop-dev" not in cmd \
            and "AWS_PROFILE" not in cmd:
        print("BLOQUEADO por guard_aws.py: usa --profile workshop-dev (o AWS_PROFILE=workshop-dev).",
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
