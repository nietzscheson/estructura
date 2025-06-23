#!/usr/bin/env bash
set -euo pipefail

echo $ENVIRONMENT

SECRET_ID="estructura-$ENVIRONMENT"

echo "[env] Loading secrets from $SECRET_ID..."

# Obtener el JSON desde AWS Secrets Manager
SECRETS_JSON=$(aws secretsmanager get-secret-value \
  --secret-id "$SECRET_ID" \
  --query 'SecretString' \
  --output text)

# Exportar cada key=value como variable de entorno
echo "$SECRETS_JSON" | jq -r 'to_entries[] | "\(.key)=\(.value)"' | while IFS='=' read -r key value; do
  export "$key=$value"
done