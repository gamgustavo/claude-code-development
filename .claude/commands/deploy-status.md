---
description: Estado del pipeline CI/CD y del servicio ECS
allowed-tools: Bash(aws codepipeline get-pipeline-state:*), Bash(aws ecs describe-services:*), Bash(bash scripts/service_url.sh)
---

1. `aws codepipeline get-pipeline-state --name ccd-orders-api --profile workshop-dev --region us-east-1`: estado de Source, BuildAndTest y Deploy.
2. `aws ecs describe-services --cluster ccd-cluster --services ccd-orders-api --profile workshop-dev --region us-east-1`: desiredCount vs runningCount, imagen vigente.
3. `bash scripts/service_url.sh` y reporta la URL.
4. Presenta una tabla corta y, si algo falla, la causa probable.
