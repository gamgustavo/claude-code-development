#!/usr/bin/env bash
# Despliega (o actualiza) la infraestructura del curso. Idempotente.
set -euo pipefail
export AWS_PROFILE="${AWS_PROFILE:-workshop-dev}" AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
CONNECTION_ARN="${CONNECTION_ARN:-arn:aws:codeconnections:us-east-1:471112715746:connection/ca0d02d8-b47f-4661-889e-54c1496706d2}"
cd "$(dirname "$0")"

ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
[ "$ACCOUNT" = "471112715746" ] || { echo "Cuenta inesperada: $ACCOUNT"; exit 1; }

VPC=$(aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query 'Vpcs[0].VpcId' --output text)
SUBNETS=$(aws ec2 describe-subnets --filters Name=vpc-id,Values="$VPC" --query 'Subnets[].SubnetId' --output text | tr '\t' ',')

aws cloudformation deploy --stack-name ccd-base --template-file base.yml \
  --capabilities CAPABILITY_IAM --no-fail-on-empty-changeset \
  --parameter-overrides VpcId="$VPC" SubnetIds="$SUBNETS" \
  --tags proyecto=claude-code-course

out() { aws cloudformation describe-stacks --stack-name ccd-base --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" --output text; }

aws cloudformation deploy --stack-name ccd-pipeline --template-file pipeline.yml \
  --capabilities CAPABILITY_IAM --no-fail-on-empty-changeset \
  --parameter-overrides ConnectionArn="$CONNECTION_ARN" RepositoryName="$(out RepositoryName)" \
    ClusterName="$(out ClusterName)" ServiceName="$(out ServiceName)" \
  --tags proyecto=claude-code-course
echo "Listo. Pipeline: ccd-orders-api"
