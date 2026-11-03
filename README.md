# Claude Code: de la terminal al pipeline CI/CD en AWS

Curso práctico de ITZ Data. Muestra cómo desarrollar con Claude Code **dentro de un marco de gobierno estandarizado** (`CLAUDE.md`, `standards/`, permisos, hooks, skills y comandos) y llevar el resultado a producción con servicios AWS de bajo costo.

## Flujo que se demuestra
```
prompt → plan → código + tests → git push (GitHub)
      → CodePipeline (CodeConnections) → CodeBuild (pytest + docker build)
      → ECR (escaneo) → ECS Fargate → CloudWatch Logs → incidente → diagnóstico con Claude
```

## Temario (7 módulos)
| # | Módulo | Guía |
|---|---|---|
| 1 | Instalación y configuración (npm, macOS, Ubuntu/Debian, Windows + WSL) | [modulos/01_instalacion](modulos/01_instalacion/README.md) |
| 2 | Uso desde la CLI: escribir, editar, refactorizar, tests y documentación | [modulos/02_cli_codigo](modulos/02_cli_codigo/README.md) |
| 3 | Análisis de codebases, revisión de PRs y Git | [modulos/03_codebase_git_prs](modulos/03_codebase_git_prs/README.md) |
| 4 | Docker, contenedores, Kubernetes, YAML, scripts y CI/CD | [modulos/04_docker_k8s_cicd](modulos/04_docker_k8s_cicd/README.md) |
| 5 | Diagnóstico de incidentes con logs y configuración | [modulos/05_incidentes](modulos/05_incidentes/README.md) |
| 6 | MCP, GitHub, búsqueda web y búsqueda en codebases | [modulos/06_mcp_github](modulos/06_mcp_github/README.md) |
| 7 | Gestión de contexto, modo plan, comandos y automatizaciones | [modulos/07_contexto_automatizacion](modulos/07_contexto_automatizacion/README.md) |

## Estructura
| Ruta | Contenido |
|---|---|
| `app/`, `tests/` | API de pedidos (Flask) y pruebas |
| `Dockerfile`, `k8s/` | Contenedor y manifiestos Kubernetes de referencia |
| `buildspec.yml`, `infra/` | CodeBuild + CloudFormation (ECR, ECS Fargate, CodePipeline) |
| `.claude/`, `CLAUDE.md`, `standards/` | Marco de gobierno: permisos, hooks, skills, comandos, estándares |
| `scripts/` | Utilidades (validar YAML, URL del servicio, `selftest_governance.py`) |
| `docs/GUION_PRUEBAS.md` | Corrida de pruebas de cada herramienta de Claude configurada |

## Costo y limpieza
Fargate 0.25 vCPU / 0.5 GB con IP pública, **sin ALB, NAT ni EKS** (≈ USD 0.3/día). Kubernetes se enseña con manifiestos validados localmente. Al terminar: `bash infra/destroy.sh`.

## Puesta en marcha (instructor)
1. `aws configure --profile workshop-dev` (cuenta `471112715746`, `us-east-1`).
2. Crear/autorizar la conexión GitHub en CodeConnections (ya existe: `claude-code-development`).
3. `git push origin main` y luego `bash infra/deploy.sh`.
4. `bash scripts/service_url.sh` para obtener la URL y probar `/health` y `/orders`.
