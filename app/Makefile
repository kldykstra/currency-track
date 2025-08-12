# Currency Track Project Makefile

.PHONY: deploy dev

# Deploy with the deploy.sh script
deploy:
	@echo "Deploying with the deploy.sh script..."
	./deploy.sh


# Run locally for development
dev:
	@./dev.sh

# Stop and remove containers
down:
	@echo "Stopping and removing containers..."
	docker-compose -f compose.yaml down --volumes --rmi all
	@echo "Containers stopped and removed."
