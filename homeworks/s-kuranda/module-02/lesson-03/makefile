#!make

include .env

default: help

build: ## Build docker images for service running
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) \
	  --build-arg GO_VERSION=$(GO_VERSION) \
	  -f Dockerfile $(GO_PATH)

build-no-cached: ## Build docker images for service running without cached layers
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) \
	  --build-arg GO_VERSION=$(GO_VERSION) \
	  -f Dockerfile $(GO_PATH) --no-cache

start: ## Start our app
	docker run --rm -d -p 127.0.0.1:$(APP_EXT_PORT):8080 --name $(APP_NAME) $(IMAGE_NAME):$(IMAGE_TAG)

stop: ## Stop our app
	docker stop $(APP_NAME)

restart: ## Restart our app
	docker restart $(APP_NAME)

# makefile help
help:
	@echo "usage: make [command]"
	@echo ""
	@echo "available commands:"
	@sed \
    		-e '/^[a-zA-Z0-9_\-]*:.*##/!d' \
    		-e 's/:.*##\s*/:/' \
    		-e 's/^\(.\+\):\(.*\)/$(shell tput setaf 6)\1$(shell tput sgr0):\2/' \
    		$(MAKEFILE_LIST) | column -c2 -t -s :