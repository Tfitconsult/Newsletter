# Makefile for multi-topic newsletter repo
TOPIC ?= ev
COMPOSE := docker compose -f docker-compose.yml -f docker-compose.topic.yml

.PHONY: dev up down logs

dev: up
up:
	@export TOPIC_SLUG=$(TOPIC); $(COMPOSE) up -d --build
down:
	@export TOPIC_SLUG=$(TOPIC); $(COMPOSE) down
logs:
	@export TOPIC_SLUG=$(TOPIC); $(COMPOSE) logs -f

.PHONY: ping note
ping:
	@curl -sS http://localhost:8000/notes | jq . || curl -sS http://localhost:8000/notes
note:
	@curl -sS -X POST http://localhost:8000/notes \
	 -H 'content-type: application/json' \
	 -d '{"raw_text":"EU Parliament tightens CO2 targets"}' | jq . || true

.PHONY: render pdf
default: render
render:
	@mkdir -p build/diagrams
	@cd dev-tools && npx mmdc -i ../docs/uml/class.mmd -o ../build/diagrams/class.svg
	@cd dev-tools && npx mmdc -i ../docs/uml/flow.mmd -o ../build/diagrams/flow.svg
	@echo "PlantUML: run java -jar plantuml.jar -tsvg -o ../../build/diagrams docs/uml/usecase.puml"

pdf:
	@. ./.venv/bin/activate && python scripts/build_manual_pdf.py && echo "Wrote build/cancanary_dev_manual.pdf"

.PHONY: topic topic-example

# Scaffold new topic
# Usage: make topic TOPIC=newtopic

topic:
	@python3 scripts/new_topic.py $(TOPIC)
	@echo "Now edit topics/$(TOPIC)/.env and brand.json"

.PHONY: clean
clean:
	rm -rf build dist .venv node_modules dev-tools/node_modules plantuml.jar
