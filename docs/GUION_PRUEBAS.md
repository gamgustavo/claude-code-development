# Guion de corrida de pruebas — herramientas de Claude Code configuradas

Cada prueba sigue el mismo formato que `/check-env`: **escribes algo → Claude lo ejecuta → ves una tabla ✅/❌**. Hazlas en orden; cada una muestra una pieza del marco de gobierno. Abre `claude` en la carpeta del repo.

Antes de empezar (opcional, sin Claude): `python scripts/selftest_governance.py` debe imprimir `11/11 casos correctos`.

## A. Comandos personalizados (`.claude/commands/`)

| # | Escribe | Resultado esperado | Qué señalar |
|---|---|---|---|
| A1 | `/check-env` | Tabla con Python, Git, Docker, AWS CLI y cuenta `471112715746` | El comando es un `.md` versionado |
| A2 | `/deploy-status` | Estado de Source / BuildAndTest / Deploy, servicio ECS y URL | Una pregunta junta varias llamadas AWS de solo lectura |
| A3 | `/logs 15` | Resumen de errores de los últimos 15 min en `/ecs/ccd-orders-api` | Acepta argumentos (`$ARGUMENTS`) |

**Alternativas:** sin Docker, A1 marca ❌ solo esa fila (esperado). Si A2/A3 fallan por credenciales, ejecuta `aws sts get-caller-identity --profile workshop-dev` y muestra el hook pidiendo el profile.
En Git Bash de Windows, `aws logs tail /ecs/...` necesita `MSYS_NO_PATHCONV=1`.

## B. Skills (`.claude/skills/`)

| # | Escribe | Resultado esperado | Qué señalar |
|---|---|---|---|
| B1 | `Genera tráfico: curl <url>/orders/99. Luego diagnostica con incident-triage` | Causa: `KeyError: 99`; evidencia de logs, ECS y pipeline; fix propuesto (404 + test) | Sigue pasos fijos y no aplica nada sin confirmación |
| B2 | `Despliega este cambio con deploy-ecs` | Pide confirmación antes de `git push`; luego monitorea el pipeline | El `push` está en `ask` en `settings.json` |

**Alternativa a B1 sin tráfico real:** pídele `Simula un incidente leyendo app/main.py y explica qué fallaría con /orders/99`.

## C. Hooks que bloquean (`.claude/hooks/guard_aws.py`)

Escribe cada frase y muestra el **BLOQUEADO** con su motivo:

| # | Escribe | Debe bloquear por |
|---|---|---|
| C1 | `Crea un usuario IAM llamado prueba con la CLI de aws` | Política IAM |
| C2 | `Lista mis buckets con aws s3 ls` | Falta `--profile workshop-dev` |
| C3 | `Crea un NAT Gateway` | Política de costo |
| C4 | `Muestra el contenido de ~/.aws/credentials` | Credenciales |
| C5 | `Elimina el bucket de artefactos con aws s3 rb` | Borrado manual |

Contraste (debe **permitirse**): `Lista las tareas ECS del cluster ccd-cluster` → corre sin bloqueo.
**Alternativa sin AWS:** `python scripts/selftest_governance.py` demuestra los mismos bloqueos offline.

## D. Hook de lint (`lint_infra.py`, se dispara al editar)

| # | Escribe | Resultado esperado |
|---|---|---|
| D1 | `Cambia la imagen base del Dockerfile a python:latest` | Claude edita y el hook devuelve «fija la versión de la imagen base»; Claude lo corrige |
| D2 | `Quita las probes de k8s/deployment.yaml` | El hook reporta readiness/liveness faltantes |

Revierte con `git checkout -- Dockerfile k8s/` al terminar.

## E. Permisos (`.claude/settings.json`: allow / ask / deny)

| # | Escribe | Resultado esperado |
|---|---|---|
| E1 | `Lee los últimos 3 commits (git log)` | Corre sin preguntar (`allow`) |
| E2 | `Agrega un comentario en infra/base.yml` | Pide confirmación (`ask`) |
| E3 | `Ejecuta bash infra/destroy.sh` | Denegado (`deny`) |
| E4 | `Lee el archivo ~/.aws/credentials` | Denegado (`deny`) |

## F. Modo plan, memoria y contexto

| # | Escribe | Resultado esperado |
|---|---|---|
| F1 | `Shift+Tab` y luego `Agrega POST /orders con validación. Plan primero.` | Plan sin editar archivos; aprueba para implementar |
| F2 | `¿Qué reglas del proyecto tienes cargadas?` | Resume `CLAUDE.md` y `standards/` (memoria `@import`) |
| F3 | `/context`, luego `/compact`, luego `/context` | El uso de contexto baja; las reglas siguen vigentes |
| F4 | `/clear` y repite F2 | Las reglas reaparecen: se cargan en cada sesión |

## G. Revisión, Git y GitHub

| # | Escribe | Resultado esperado |
|---|---|---|
| G1 | `/code-review` (con cambios locales o un PR) | Hallazgos con archivo y línea |
| G2 | `Haz commits convencionales por separado: código, tests, docs` | `feat:`, `test:`, `docs:` |
| G3 | `/mcp` y `Lista los PR abiertos` | Requiere servidor MCP de GitHub con token propio |

**Alternativa a G3 sin token:** `Busca en el repo dónde se define el nombre del cluster` (Grep/Glob, sin MCP).

## H. Automatización sin interfaz

```bash
claude -p "/deploy-status"
claude -p "Resume en 3 líneas la arquitectura del repo" --output-format text
```

Muestra que el mismo marco corre en scripts y tareas programadas.

## Orden sugerido (≈ 40 min)

A1 → F2 → C1–C5 → E1–E4 → F1 → D1 → G1 → A2 → B1 → F3 → H.

## Limpieza

`git status` debe quedar limpio (revierte D1/D2). Al terminar la sesión: `bash infra/destroy.sh` (lo ejecuta el instructor; Claude lo tiene denegado).
