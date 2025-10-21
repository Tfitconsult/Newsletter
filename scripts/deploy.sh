#!/usr/bin/env bash
set -euo pipefail
: "${TOPIC_SLUG:?TOPIC_SLUG not set. export TOPIC_SLUG=<ev|tfktcl|tfitconsult|...>}"
echo "Deploying topic: $TOPIC_SLUG"
docker compose -f docker-compose.yml -f docker-compose.topic.yml up -d --build
