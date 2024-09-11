Example application that leverage LLAMA3.1 for sentiment analysis

# Requirements
- docker
- docker compose pluging [installation](https://docs.docker.com/compose/install/linux/)

# Commands:
- **api-docs**: Creates swagger ui instance with api documentation
- **api**: Start api server
- **help**: Show help for each of the Makefile recipes
- **predict**: Predict and creates results.json
- **process-features**: Preprocess features and creates Data/features.csv file
- **pull-model**: Download weights for model, need to run only once after container starts
- **start**: Start Docker Compose services
- **test**: Run tests in docker container

# Quick Start

Follow these steps in order:

## Start Ollama server

`make start` 

this will start ollama server that will run llama3.1 model

## Download llama3.1 weights (needs to be done only once)

`make pull-model` 

this will dowload the weights to *models* folder

## Process features

`make process-features`

this will generate *features.csv* in Data folder

## Start API

`make api`

this will spin up api with url localhost:5000

## Run predict

`make predict`

this will run predict script and generate results.json


# Additional Commands

## Api docs

`make api-docs`

run swagger-ui to view api documentation (localhost:8080)

## Tests

`make test`

runs test using pytest in a docker container


# Example payload

after running all the commands in quick start, you can use curl to test api

```bash
curl localhost:5000/decision/v1 -XPost -H "Content-Type: application/json"   -d '{
"ride_id": "RIDE2",
"drone_id": "DRONE5",
"timestamp": "2024-08-11T16:45:29.123456+00:00",
"location": "Midtown",
"weather_conditions": "Storm",
"customer_query": "Why is the drone not here yet?"
}'

```

