#!/usr/bin/env python
"""Hook PostToolUse (Write|Edit) — lint de Dockerfile y YAML contra standards/docker-k8s.md.

exit 2 devuelve el hallazgo a Claude para que lo corrija.
"""
import json
import os
import re
import sys


def check(path: str, text: str) -> list[str]:
    name = os.path.basename(path)
    issues = []
    if name == "Dockerfile":
        if re.search(r"^FROM\s+\S+:latest\b|^FROM\s+[^:\s]+\s*$", text, re.M):
            issues.append("Dockerfile: fija la versión de la imagen base (sin :latest).")
        if not re.search(r"^USER\s+(?!root)\S+", text, re.M):
            issues.append("Dockerfile: falta USER no root.")
        if "HEALTHCHECK" not in text:
            issues.append("Dockerfile: falta HEALTHCHECK.")
    norm = path.replace("\\", "/")
    if "/k8s/" in norm and name.endswith((".yaml", ".yml")) and "kind: Deployment" in text:
        for needle, msg in [("resources:", "resources requests/limits"), ("readinessProbe", "readinessProbe"),
                            ("livenessProbe", "livenessProbe"), ("runAsNonRoot", "runAsNonRoot")]:
            if needle not in text:
                issues.append(f"k8s: Deployment sin {msg}.")
        if re.search(r"image:\s*\S+:latest", text):
            issues.append("k8s: imagen con :latest no permitida.")
    return issues


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    path = (payload.get("tool_input") or {}).get("file_path", "")
    if not path or not os.path.isfile(path):
        return 0
    with open(path, encoding="utf-8", errors="replace") as fh:
        issues = check(path, fh.read())
    if issues:
        print("lint_infra.py:\n- " + "\n- ".join(issues), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
