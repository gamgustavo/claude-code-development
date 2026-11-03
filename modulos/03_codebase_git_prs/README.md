# Módulo 3 — Análisis de codebases, revisión de PRs y Git

## Ejercicio 1: entender el repo
*«Explícame la arquitectura de este repo y el recorrido de un `git push` hasta producción»* — Claude debe citar `buildspec.yml`, `infra/pipeline.yml` y `app/main.py`.

## Ejercicio 2: Git y PR
1. `git switch -c feat/post-orders`; cambios del módulo 2.
2. *«Haz commits convencionales por separado (código, tests, docs)»*.
3. `git push -u origin feat/post-orders` y abrir el PR en GitHub.
4. `/code-review` sobre el diff: buscar bugs (p. ej. `GET /orders/<id>` falla con 500 si no existe).

## Criterios de revisión (gobierno)
Tests incluidos, sin secretos, YAML válido (`python scripts/validate_yaml.py`), sin recursos fuera de `ccd-`.
