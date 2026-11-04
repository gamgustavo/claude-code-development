---
description: Revisa Dockerfile y manifiestos k8s/ contra standards/docker-k8s.md (solo lectura)
allowed-tools: Read, Grep, Glob, Bash(python scripts/validate_yaml.py)
---

Revisa el contenedor del proyecto contra `standards/docker-k8s.md`. No modifiques ningún archivo.

1. Lee `Dockerfile`, `.dockerignore`, `requirements.txt` y `k8s/*.yaml`.
2. Comprueba cada regla del estándar: imagen base fija desde `public.ecr.aws` (nunca `latest`), usuario no root, `HEALTHCHECK`, sin secretos, `.dockerignore`, dependencias fijadas, `labels`, `resources`, probes, `runAsNonRoot` e imagen con etiqueta explícita.
3. Ejecuta `python scripts/validate_yaml.py` y reporta su resultado.
4. Presenta una tabla con regla, archivo, estado (cumple o incumple) y, si incumple, la corrección propuesta.
5. Pregunta si quieres que aplique las correcciones; no las apliques sin confirmación.
