#!/bin/bash
set -e
export KUBECONFIG=/tmp/k3s.yaml

LISTMONK_CLIENT_ID="$1"
LISTMONK_CLIENT_SECRET="$2"
AUTHENTIK_URL="$3"
LISTMONK_URL="$4"

echo "Waiting for Listmonk deployment to be fully available (prevent init container race condition)..."
kubectl rollout status deployment listmonk -n listmonk --timeout=600s

# Double check database is responsive just in case
for i in {1..12}; do
  if kubectl exec -n listmonk statefulset/listmonk-postgres -- psql -U listmonk -d listmonk -t -c 'SELECT 1 FROM settings LIMIT 1;' > /dev/null 2>&1; then
    echo "Listmonk DB is ready."
    break
  fi
  sleep 5
done

OIDC_JSON='{"enabled": true, "client_id": "'${LISTMONK_CLIENT_ID}'", "provider_url": "'${AUTHENTIK_URL}'/application/o/listmonk/", "client_secret": "'${LISTMONK_CLIENT_SECRET}'", "provider_name": "Authentik", "auto_create_users": true, "default_list_role_id": null, "default_user_role_id": 1}'

# Update the settings table
kubectl exec -n listmonk statefulset/listmonk-postgres -- psql -U listmonk -d listmonk -c "UPDATE settings SET value = '${OIDC_JSON}' WHERE key = 'security.oidc';"
kubectl exec -n listmonk statefulset/listmonk-postgres -- psql -U listmonk -d listmonk -c "UPDATE settings SET value = '\"${LISTMONK_URL}\"' WHERE key = 'app.root_url';"

# Force the root URL as an environment variable in case the DB setting is ignored
kubectl set env deployment listmonk -n listmonk LISTMONK_app__root_url="${LISTMONK_URL}"

# Restart Listmonk to apply the settings if needed
kubectl rollout restart deployment listmonk -n listmonk
kubectl rollout status deployment listmonk -n listmonk --timeout=300s
