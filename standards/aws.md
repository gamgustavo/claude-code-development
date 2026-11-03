# Estándar AWS

| Tema | Regla |
|---|---|
| Cuenta / profile | `471112715746` / `workshop-dev`; región `us-east-1` |
| Nombres | `ccd-<recurso>`, minúsculas con guiones (`ccd-orders-api`, `ccd-cluster`) |
| Tags | `proyecto=claude-code-course` en todo lo que lo soporte |
| IaC | CloudFormation en `infra/`; nada creado "a mano" en la consola |
| Despliegue | Solo vía pipeline (`git push` a `main`) o `infra/deploy.sh` |
| Permisos | Roles IAM de mínimo privilegio; sin `*:*`; sin usuarios nuevos |
| Logs | CloudWatch, retención 3 días; logs en JSON a stdout |
| Imágenes | Etiqueta = SHA corto del commit; nunca `latest`; escaneo al subir |
| Costo | Fargate 0.25 vCPU / 0.5 GB, 1 tarea, IP pública; sin ALB/NAT/EKS |
| Limpieza | `infra/destroy.sh` al terminar |
