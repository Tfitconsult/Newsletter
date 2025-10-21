# CanCanary Multi-Topic Newsletter Stack

Reusable architecture for multiple newsletter topics (EV, TFKTCL, TFIT Consult).
Switch topics by setting `TOPIC_SLUG` and per-topic `.env`, brand, DB and SMTP settings.

## Quick start
```bash
# Build and run for EV topic
export TOPIC_SLUG=ev
docker compose -f docker-compose.yml -f docker-compose.topic.yml up -d
```

## Topics
- `topics/ev`  (cancanary.de)
- `topics/tfktcl` (tfktcl.de)
- `topics/tfitconsult` (tfitconsult.de)

## CI
- `docs.yml`: renders Mermaid/PlantUML diagrams and builds a combined PDF manual
- `deploy.yml`: matrix build across topics

## Local dev tools
- Python 3.11 virtualenv at `.venv`
- Node tools in `dev-tools/` (MJML + Mermaid CLI)
