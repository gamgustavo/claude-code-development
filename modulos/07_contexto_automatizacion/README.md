# Módulo 7 — Contexto, planificación, comandos y automatizaciones

Todo el marco de gobierno de este repo vive en archivos versionados:

| Pieza | Archivo | Para qué |
|---|---|---|
| Memoria de proyecto | `CLAUDE.md`, `standards/*.md` | Reglas siempre en contexto (`@import`) |
| Permisos | `.claude/settings.json` | allow / ask / deny por herramienta |
| Hooks | `.claude/hooks/guard_aws.py`, `lint_infra.py` | Bloquean antes y revisan después de actuar |
| Comandos | `.claude/commands/` | `/check-env`, `/logs`, `/deploy-status` |
| Skills | `.claude/skills/` | `deploy-ecs`, `incident-triage` |
| Modo plan | `Shift+Tab` | Planificar antes de ejecutar |

## Ejercicios
1. Gestión de contexto: `/context`, `/compact` y `/clear`; ¿qué conviene dejar en `CLAUDE.md` frente a pedirlo en el prompt?
2. Prueba negativa de hooks: pedir *«crea un usuario IAM»* y *«lista buckets sin profile»* → deben bloquearse con el motivo.
3. Crear un comando nuevo `/costos` que liste recursos `ccd-` y estime costo diario.
4. Crear un hook que impida `git push` si fallan los tests.
5. Automatización: `claude -p "/deploy-status"` desde un script o tarea programada.
