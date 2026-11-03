# CLAUDE.md — Curso Claude Code: de la terminal al pipeline CI/CD en AWS

Memoria de proyecto que Claude Code carga al iniciar. Define el **marco de gobierno**: se puede desarrollar rápido, pero dentro de reglas fijas.

@standards/aws.md
@standards/docker-k8s.md

## Contexto
- App de ejemplo: API de pedidos Flask (`app/`), tests en `tests/`.
- Despliegue: GitHub → CodePipeline (CodeConnections) → CodeBuild → ECR → ECS Fargate. IaC en `infra/`.
- Cuenta AWS del curso: `471112715746`, profile `workshop-dev`, región `us-east-1`.

## Reglas obligatorias
1. Usa **siempre** `--profile workshop-dev`/`AWS_PROFILE=workshop-dev`; verifica la cuenta antes de cambiar nada.
2. Todo recurso con prefijo `ccd-` y tag `proyecto=claude-code-course`.
3. Solo lectura por defecto en AWS. Cambios solo por `infra/deploy.sh` o por el pipeline (git push). Prohibido IAM, borrados manuales y recursos fuera de `ccd-`.
4. Nunca leas ni imprimas credenciales (`~/.aws/credentials`, `*accessKeys*.csv`).
5. Plan primero (Shift+Tab, modo plan) antes de crear infraestructura. Commits convencionales (`feat:`, `fix:`, `docs:`).
6. Cada cambio de código lleva test; `pytest` y `python scripts/validate_yaml.py` deben pasar antes del commit.
7. Costos: sin ALB, NAT ni EKS. Termina las sesiones con `infra/destroy.sh` si no se seguirá usando.
8. Responde en español.

## Flujo
`/check-env` → plan → código + tests → `git push` → pipeline → `/logs` → `/deploy-status`. Hooks en `.claude/hooks/` bloquean comandos AWS fuera de política y lintean YAML/Dockerfile.
