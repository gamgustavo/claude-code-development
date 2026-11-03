# Módulo 4 — Docker, Kubernetes, YAML y CI/CD en AWS

## Arquitectura
```
GitHub (main) ─▶ CodePipeline ─▶ CodeBuild ─▶ ECR (ccd-orders-api:<sha>) ─▶ ECS Fargate (ccd-cluster)
   CodeConnections   Source→BuildAndTest→Deploy    pytest + docker build        1 tarea, IP pública
```
Plantillas: `infra/base.yml` (ECR, logs, cluster, task, servicio) e `infra/pipeline.yml` (bucket, CodeBuild, CodePipeline).

## Ejercicios
1. **Docker:** *«Revisa el Dockerfile contra standards/docker-k8s.md»*. Local (si hay Docker): `docker build -t orders .` y `docker run -p 8080:8080 orders`.
2. **Kubernetes:** *«Agrega un `HorizontalPodAutoscaler` en `k8s/` y valida el YAML»*. Se valida con `python scripts/validate_yaml.py`; no se usa EKS por costo (≈ USD 73/mes).
3. **CI/CD:** cambiar la versión del mensaje de `/health`, `git push` y seguir con `/deploy-status` hasta que Deploy sea `Succeeded`.
4. **Verificación:** `bash scripts/service_url.sh` → `curl <url>/health`.
5. **Scripts:** leer `infra/deploy.sh` y `infra/destroy.sh`; ¿por qué son idempotentes y verifican la cuenta?

## Limpieza
`bash infra/destroy.sh`
