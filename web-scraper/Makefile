# Makefile for web-scraper

.PHONY: test-local deploy invoke

# Run the local test script
test-local:
	source ./scripts/aws.sh && \
	bash ./scripts/test_local.sh

# Package and deploy the lambda function

deploy:
	source ./scripts/aws.sh && \
	bash ./scripts/deploy.sh

# Invoke the deployed lambda function

invoke:
	source ./scripts/aws.sh && \
	bash ./scripts/invoke.sh currencyTrackScraperProd 