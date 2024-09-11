default: help

.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# Targets
.PHONY: start pull-model api test process-features predict api-docs

start: # Start Docker Compose services
	docker compose up

pull-model: # Download wheights for model, need to run only one after container starts
	docker compose exec -it ollama ollama pull llama3.1

api: # Start api server
	docker compose up api -d
	echo api started - localhost:5000

test: # Run tests in docker container
	docker compose run test

process-features: # Preprocess features and creates Data/features.csv file
	docker compose run process-features

predict: # Predict and creates results.json
	docker compose run predict

api-docs: # Creates swagger ui instance with api documentation
	docker compose up -d api-docs
	echo go to localhost:8080 to view api documentation
