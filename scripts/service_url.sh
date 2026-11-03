#!/usr/bin/env bash
# Imprime la URL pública de la tarea Fargate (IP pública, sin ALB).
set -euo pipefail
export AWS_PROFILE="${AWS_PROFILE:-workshop-dev}" AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
TASK=$(aws ecs list-tasks --cluster ccd-cluster --service-name ccd-orders-api --query 'taskArns[0]' --output text)
ENI=$(aws ecs describe-tasks --cluster ccd-cluster --tasks "$TASK" \
  --query "tasks[0].attachments[0].details[?name=='networkInterfaceId'].value" --output text)
IP=$(aws ec2 describe-network-interfaces --network-interface-ids "$ENI" --query 'NetworkInterfaces[0].Association.PublicIp' --output text)
echo "http://$IP:8080"
