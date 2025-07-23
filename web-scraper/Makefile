# Makefile for web-scraper

.PHONY: setup test deploy invoke

setup:
	source ./.env && \
	bash ./scripts/aws.sh && \
	bash ./scripts/dev_setup.sh

# Run the local test script
test:
	source ./.env && \
	bash ./scripts/aws.sh && \
	bash ./scripts/test_local.sh

# Package and deploy the lambda function

deploy:
	source ./.env && \
	bash ./scripts/aws.sh && \
	bash ./scripts/deploy.sh

# Invoke the deployed lambda function

invoke:
	source ./.env && \
	bash ./scripts/aws.sh && \
	bash ./scripts/invoke.sh currencyTrackScraperProd 