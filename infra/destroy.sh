#!/usr/bin/env bash
# Teardown del demo: deja la cuenta limpia (solo recursos con prefijo ccd-).
set -euo pipefail
export AWS_PROFILE="${AWS_PROFILE:-workshop-dev}" AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
[ "$ACCOUNT" = "471112715746" ] || { echo "Cuenta inesperada: $ACCOUNT"; exit 1; }

BUCKET="ccd-pipeline-artifacts-${ACCOUNT}-${AWS_DEFAULT_REGION}"
aws s3 rm "s3://$BUCKET" --recursive 2>/dev/null || true
aws cloudformation delete-stack --stack-name ccd-pipeline
aws cloudformation wait stack-delete-complete --stack-name ccd-pipeline
# ECR con imágenes: se vacía antes de borrar el stack base
aws ecr batch-delete-image --repository-name ccd-orders-api \
  --image-ids "$(aws ecr list-images --repository-name ccd-orders-api --query 'imageIds[*]' --output json)" >/dev/null 2>&1 || true
aws cloudformation delete-stack --stack-name ccd-base
aws cloudformation wait stack-delete-complete --stack-name ccd-base
echo "Teardown completo."
