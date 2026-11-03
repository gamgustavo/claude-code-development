# Estándar Docker y Kubernetes

## Dockerfile
- Imagen base slim desde `public.ecr.aws` (evita límites de Docker Hub); versión fija, nunca `latest`.
- Usuario no root (`USER appuser`), `HEALTHCHECK`, sin secretos en capas, `.dockerignore` presente.
- Dependencias fijadas en `requirements.txt`.

## Manifiestos Kubernetes (`k8s/`)
- `labels.app` y `labels.proyecto` en todo objeto.
- `resources.requests/limits`, `readinessProbe` y `livenessProbe` obligatorios.
- `securityContext.runAsNonRoot: true`.
- Imagen con etiqueta explícita (SHA), no `latest`.
- Se validan localmente (`python scripts/validate_yaml.py`); el clúster EKS queda fuera del demo por costo.
