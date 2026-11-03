---
description: Lee los últimos logs de la app en CloudWatch y resume errores
argument-hint: [minutos, por defecto 15]
allowed-tools: Bash(aws logs tail:*), Bash(aws logs filter-log-events:*)
---

Lee los logs de `/ecs/ccd-orders-api` de los últimos ${ARGUMENTS:-15} minutos:

`aws logs tail /ecs/ccd-orders-api --since 15m --profile workshop-dev --region us-east-1`

Resume: errores (`ERROR`, `Traceback`), frecuencia y endpoint afectado. Si hay un incidente, sigue el skill `incident-triage`.
