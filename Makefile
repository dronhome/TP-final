# ==========================================
# Makefile for Multi-Service Project
# ==========================================

REGISTRY ?= berserkchmonya
TAG ?= latest
SERVICES = web team19-web nao-robot-api skeleton-finder-api translator

# ------------------------------------------
#          HELP (auto-generated)
# ------------------------------------------
.PHONY: help
help:  ## Show this help message
	@echo ""
	@echo "📌 Available commands:"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z0-9_.-]+:.*##/ { printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""

# ------------------------------------------
#          IMAGE MANAGEMENT
# ------------------------------------------
build-all: ## Build all Docker images
	@echo "Building all Docker images..."
	docker-compose -f docker-compose.build.yml build

build-%: ## Build a single service (usage: make build-web)
	@echo "Building $*..."
	docker-compose -f docker-compose.build.yml build $*

push-all: ## Push all images to registry
	@echo "Pushing images to registry..."
	@for service in $(SERVICES); do \
		image=$(REGISTRY)/$$service:$(TAG); \
		echo "Pushing $$image"; \
		docker push $$image || echo "Failed to push $$image"; \
	done

check-images: ## Check if all local images exist
	@echo "Checking local images..."
	@for service in $(SERVICES); do \
		image=$(REGISTRY)/$$service:$(TAG); \
		if docker image inspect $$image >/dev/null 2>&1; then \
			echo "✓ $$image"; \
		else \
			echo "✗ $$image - not found"; \
		fi \
	done

# ------------------------------------------
#     DEVELOPMENT (Docker Compose)
# ------------------------------------------
dev-up: build-all ## Start development environment (build + run)
	@echo "Starting development environment..."
	docker-compose -f docker-compose.dev.yml up -d
	@echo ""
	@echo "🌐 Services:"
	@echo "  - web:                http://localhost:8080"
	@echo "  - team19-web:         http://localhost:3000"
	@echo "  - nao-robot-api:      http://localhost:5000"
	@echo "  - skeleton-finder-api: http://localhost:6001"
	@echo "  - translator:         http://localhost:7000"

dev-down: ## Stop development environment
	@echo "Stopping development environment..."
	docker-compose -f docker-compose.dev.yml down

dev-logs: ## Show dev logs (real-time)
	docker-compose -f docker-compose.dev.yml logs -f

dev-restart: dev-down dev-up ## Restart dev environment

# ------------------------------------------
#                 TESTING
# ------------------------------------------
test: ## Test all services locally
	@echo "Testing services..."
	@curl -sSf http://localhost:8080/ >/dev/null && echo "✓ web (8080)" || echo "✗ web"
	@curl -sSf http://localhost:3000/ >/dev/null && echo "✓ team19-web (3000)" || echo "✗ team19-web"
	@curl -sSf http://localhost:5000/ >/dev/null && echo "✓ nao-robot-api (5000)" || echo "✗ nao-robot-api"
	@curl -sSf http://localhost:6001/ >/dev/null && echo "✓ skeleton-finder-api (6001)" || echo "✗ skeleton-finder-api"
	@curl -sSf http://localhost:7000/test >/dev/null && echo "✓ translator (7000)" || echo "✗ translator"

# ------------------------------------------
#                 CLEANUP
# ------------------------------------------
clean: ## Remove all containers + volumes + images
	@echo "Cleaning up..."
	docker-compose -f docker-compose.dev.yml down -v
	@for service in $(SERVICES); do \
		image=$(REGISTRY)/$$service:$(TAG); \
		echo "Removing image $$image"; \
		docker rmi $$image 2>/dev/null || true; \
	done
	@echo "Cleanup complete!"

status: ## Show running Docker Compose services
	@echo "=== Running Containers ==="
	@docker-compose -f docker-compose.dev.yml ps

# ------------------------------------------
#               KUBERNETES
# ------------------------------------------
k8s-deploy: build-all ## Deploy all services to Kubernetes
	@echo "Deploying to Kubernetes..."
	kubectl apply -f k8s/
	@kubectl wait --for=condition=available deployment/web-deployment --timeout=120s 2>/dev/null || true
	@kubectl wait --for=condition=available deployment/team19-web-deployment --timeout=120s 2>/dev/null || true
	@kubectl wait --for=condition=available deployment/naorobotapi-deployment --timeout=120s 2>/dev/null || true
	@kubectl wait --for=condition=available deployment/skeletonfinderapi-deployment --timeout=120s 2>/dev/null || true
	@echo "k8s deploy done"

k8s-delete: ## Delete all Kubernetes resources
	@echo "Removing from Kubernetes..."
	kubectl delete -f k8s/ --ignore-not-found=true

k8s-logs: ## Print logs from all Kubernetes pods
	@kubectl logs -l app=web --tail=100 || true
	@kubectl logs -l app=team19-web --tail=100 || true
	@kubectl logs -l app=naorobotapi --tail=100 || true
	@kubectl logs -l app=skeletonfinderapi --tail=100 || true

k8s-status: ## Show status of all Kubernetes pods/services
	@kubectl get nodes || true
	@kubectl get deployments,services,pods -o wide || true

k8s-get-urls: ## Show all Kubernetes service URLs
	@kubectl get svc -o wide || true

k8s-restart: ## Restart all Kubernetes deployments
	@kubectl rollout restart deployment web-deployment || true
	@kubectl rollout restart deployment team19-web-deployment || true
	@kubectl rollout restart deployment naorobotapi-deployment || true
	@kubectl rollout restart deployment skeletonfinderapi-deployment || true
