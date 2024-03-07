#!make
APP_HOST ?= 0.0.0.0
APP_PORT ?= 8080
EXTERNAL_APP_PORT ?= ${APP_PORT}

run = docker-compose \
	run \
	-p ${EXTERNAL_APP_PORT}:${APP_PORT} \
	-e PY_IGNORE_IMPORTMISMATCH=1 \
	-e APP_HOST=${APP_HOST} \
	-e APP_PORT=${APP_PORT} \
	app-pgstac

.PHONY: docker-shell
docker-shell:
	$(run) /bin/bash