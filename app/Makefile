# Currency Track Project Makefile

.PHONY: deploy dev down

# Deploy with the deploy.sh script
deploy:
	@echo "Deploying with the deploy.sh script..."
	./deploy.sh

# Run locally for development
dev:
	@echo "Running locally for development..."
	@./dev.sh

# Stop and remove containers
down:
	@echo "Stopping and removing containers..."
	docker-compose -f compose.yaml down --volumes --rmi all
	@echo "Containers stopped and removed."
