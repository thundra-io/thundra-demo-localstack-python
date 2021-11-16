export SERVICES = serverless,cloudformation,sts,sqs,dynamodb,s3,sns
export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION ?= us-east-1
export START_WEB ?= 1
export THUNDRA_APIKEY = <your_Thundra_apikey>
export THUNDRA_AGENT_TEST_PROJECT_ID = <your_test_project_id>
export THUNDRA_AGENT_APPLICATION_NAME = <your_application_name>

usage:              ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:            ## Install dependencies
	npm install
	which serverless || npm install -g serverless
	which localstack || pip install localstack
	which awslocal   || pip install awscli-local

test:               ## Test app
	@make install
	( \
		echo "Creating .venv..."; \
		virtualenv .venv; \
		echo "Activating .venv..."; \
		source .venv/bin/activate; \
		echo "Upgrading pip..."; \
		pip install --upgrade pip; \
		echo "Installing requirements..."; \
		pip install -r ./requirements/dev.txt; \
		echo "Starting tests..."; \
		pytest -s tests; \
		rm -rf .venv; \
		rm -rf node_modules; \
		rm -rf .serverless; \
		rm -rf .pytest_cache; \
	)

deploy:             ## Deploy the app locally
	echo "Deploying Serverless app to local environment ..."
	SLS_DEBUG=1 serverless deploy --stage local --region ${AWS_DEFAULT_REGION}

start:              ## Build, deploy and start the app locally
	@make deploy;

.PHONY: usage install deploy test start   # usage install test deploy start