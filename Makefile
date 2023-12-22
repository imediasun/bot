#!/usr/bin/make

.PHONY: help shell
.PHONY: up-postgres up-backend build-backend build-postgres
.PHONY: up down setup restart upgrade clean

.DEFAULT_GOAL : help
.SHELLFLAGS = -exc
SHELL := /bin/bash

DATABASE_DIR := ./database/
API_DIR := ./api-backend/

RAND := $(shell bash -c 'echo $$((RANDOM % 1000))' )

# This will output the help for each task. thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Show this help
	@printf "\033[33m%s:\033[0m\n" 'Available commands'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  \033[32m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

shell: ## Start shell into chat-php container
	docker-compose exec php-fpm bash


env-copy:
	cp -fa ./.env.example  ./.env


up-postgres: ## Create and start containers
	docker-compose up -d postgres

up-backend: ## Create and start containers
	docker-compose up -d backend

build-backend: ## Create and start containers
	docker-compose build backend

up: ## Create and start containers
	docker-compose up -d

down: ## Stop containers
	docker-compose down

setup: up ## Create and start containers

restart: down up ## Restart all containers

upgrade: ## Create and start containers
	make build-backend
	make up-backend

clean: ## Make clean
	docker-compose down -v # Stops containers and remove named volumes declared in the `volumes` section


