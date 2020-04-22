.PHONY: help whois nginx ionic

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

DOCKER_CMD = docker
COMPOSE_CMD = docker-compose
## All the containers names must have this prefix (this is container name in compose file)
NAME_PREFIX = chotube_

# DOCKER TASKS (for all containers)

build: ## Build the containers
	$(COMPOSE_CMD) build

up: ## Build and run the containers
	$(COMPOSE_CMD) up -d --build

start: ## Spin up the project
	$(COMPOSE_CMD) up -d

stop: ## Stop running containers
	$(COMPOSE_CMD) stop

rm: stop ## Stop and remove running containers
	$(COMPOSE_CMD) rm --force

ps: ## Display running containers
	$(DOCKER_CMD) ps

version: ## Display docker-compose version
	$(COMPOSE_CMD) --version
exec:
	$(DOCKER_CMD) docker exec -it chotube-auth-server sh


## AUTH SERVER

auth-server: ## Connect to Auth Server container
	$(DOCKER_CMD) exec -it $(NAME_PREFIX)auth-server sh

auth-server-logs: ## Display Auth Server logs
	$(DOCKER_CMD) logs -f $(NAME_PREFIX)auth-server

auth-server-start: ## Start Auth Server Container
	$(COMPOSE_CMD) start auth-server

auth-server-stop: ## Stop Auth Server Container
	$(COMPOSE_CMD) stop auth-server

auth-server-restart: ## Restart Auth Server Container
	$(COMPOSE_CMD) restart auth-server

auth-server-up: ## Build and run Ionic Container
	$(COMPOSE_CMD) up -d --build auth-server

## This could be done with all the containers.