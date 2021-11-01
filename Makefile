export SERVICES = serverless,cloudformation,sts,sqs,dynamodb,s3,sns
export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION ?= us-east-1
export START_WEB ?= 1
export THUNDRA_AGENT_DEBUG_ENABLE = true 
export THUNDRA_APIKEY = 6327942a-36ff-40a5-a840-98e71cc2af7e
export THUNDRA_AGENT_TEST_PROJECT_ID = 91596bb4-f5cf-4c28-9008-7eead02bd70f
export THUNDRA_AGENT_REPORT_REST_BASEURL = https://collector.thundra.me/v1
export THUNDRA_AGENT_APPLICATION_NAME = thundra-demo-localstack-python
export THUNDRA_AGENT_TRACE_INSTRUMENT_TRACEABLECONFIG = thundra_demo_localstack.handler.*.*[traceLineByLine=true]

usage:              ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:            ## Install dependencies
	npm install
	which serverless || npm install -g serverless
	which localstack || pip install localstack
	which awslocal   || pip install awscli-local

test:               ## Test app
	echo "Building Serverless app ..."
	pytest -s tests

deploy:             ## Deploy the app locally
	echo "Deploying Serverless app to local environment ..."
	SLS_DEBUG=1 serverless deploy --stage local --region ${AWS_DEFAULT_REGION}

start:              ## Build, deploy and start the app locally
	@make deploy;

.PHONY: usage install deploy test start   # usage install test deploy start