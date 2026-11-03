---
description: Verifica Python, Docker, AWS CLI y que el profile apunte a la cuenta del curso
allowed-tools: Bash(aws sts get-caller-identity:*), Bash(aws --version), Bash(docker --version), Bash(python --version), Bash(git --version)
---

Verifica el entorno del curso y reporta una tabla ✅/❌:

1. `python --version`, `git --version`, `docker --version`, `aws --version`.
2. `aws sts get-caller-identity --profile workshop-dev`: la cuenta debe ser `471112715746`.
3. Si algo falla, explica cómo corregirlo (sin pedir ni leer credenciales).
