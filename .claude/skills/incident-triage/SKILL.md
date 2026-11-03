---
name: incident-triage
description: Diagnostica un incidente de la API de pedidos a partir de logs de CloudWatch, estado de ECS y configuración. Úsalo cuando haya errores 5xx, la tarea reinicie o el despliegue falle.
allowed-tools: Bash(aws logs tail:*), Bash(aws logs filter-log-events:*), Bash(aws ecs describe-services:*), Bash(aws codepipeline get-pipeline-state:*), Read, Grep
---

# Triage de incidentes

1. **Síntoma**: pregunta qué se observa (endpoint, hora, mensaje).
2. **Logs**: `aws logs tail /ecs/ccd-orders-api --since 30m --profile workshop-dev --region us-east-1`; busca `ERROR`/`Traceback`.
3. **Servicio**: `aws ecs describe-services` — eventos, running vs desired, última imagen.
4. **Pipeline**: `aws codepipeline get-pipeline-state --name ccd-orders-api` — ¿el último deploy coincide con el inicio del error?
5. **Código/config**: con Grep ubica la línea responsable en `app/` o `infra/`.
6. **Informe**: causa raíz, evidencia (líneas de log), fix propuesto (diff) y test que lo cubre. No apliques nada sin confirmación.
