---
name: deploy-ecs
description: Lleva un cambio de la API a producción del demo vía GitHub → CodePipeline → ECR → ECS Fargate y verifica el resultado. Úsalo cuando se pida desplegar o publicar un cambio.
allowed-tools: Bash(python -m pytest:*), Bash(python scripts/validate_yaml.py), Bash(git:*), Bash(aws codepipeline get-pipeline-state:*), Bash(aws ecs describe-services:*), Bash(bash scripts/service_url.sh), Read
---

# Desplegar con el pipeline

1. Muestra un plan corto y espera confirmación.
2. `python -m pytest -q` y `python scripts/validate_yaml.py` deben pasar.
3. Commit convencional; `git push origin main` (pide confirmación).
4. Monitorea con `/deploy-status` hasta que Source, BuildAndTest y Deploy estén `Succeeded`.
5. `bash scripts/service_url.sh` y prueba `/health` y `/orders`.
6. Reporta imagen desplegada (SHA), URL y logs recientes. Si falla, usa el skill `incident-triage`.
