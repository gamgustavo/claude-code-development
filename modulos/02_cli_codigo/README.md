# Módulo 2 — Uso desde la CLI: código, refactor, tests y documentación

**Objetivo:** pedir cambios a Claude respetando el marco de gobierno (permisos y hooks).

## Ejercicio guiado (sobre `app/main.py`)
1. Modo plan (`Shift+Tab`): *«Agrega `POST /orders` con validación y propón el plan»*. Revisar y aprobar.
2. *«Escribe tests para el nuevo endpoint»* → `python -m pytest -q`.
3. *«Refactoriza `main.py`: separa el acceso a datos en `app/repository.py` sin cambiar el comportamiento»*; los tests deben seguir verdes.
4. *«Genera `docs/API.md` con los endpoints y ejemplos curl»*.

## Qué observar
- Los `Edit` en `app/` y `tests/` están permitidos; `infra/` y `standards/` piden confirmación (ver `.claude/settings.json`).
- Tras editar, el hook `lint_infra.py` revisa Dockerfile/k8s.
