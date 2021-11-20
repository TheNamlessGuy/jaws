THIS_FILE := $(lastword $(MAKEFILE_LIST))
include .env

# Jaws
build-jaws:
	docker build -t "${JAWS_IMAGE_NAME}:${JAWS_IMAGE_VERSION}" -f Jaws-Dockerfile .
jbuild: build-jaws

start-jaws:
	docker run "--name=${JAWS_CONTAINER_NAME}" "--network=${JAWS_NETWORK_NAME}" "--network-alias=${JAWS_NETWORK_ALIAS}" "-p=${JAWS_PORT}:8000" -d "${JAWS_IMAGE_NAME}:${JAWS_IMAGE_VERSION}"
jstart: start-jaws

stop-jaws:
	docker stop "${JAWS_CONTAINER_NAME}"
jstop: stop-jaws

clean-jaws-container: stop-jaws
	docker container rm "${JAWS_CONTAINER_NAME}"
jcclean: clean-jaws-container

# Network
start-network:
	docker network create "${JAWS_NETWORK_NAME}"
nstart: start-network

# Database
start-db:
	docker run "--name=${JAWS_DB_CONTAINER_NAME}" "--network=${JAWS_NETWORK_NAME}" "--network-alias=${JAWS_DB_NETWORK_ALIAS}" -v "${JAWS_DB_VOLUME_LOCATION}:/var/lib/postgresql/data" -e "POSTGRES_DB=${JAWS_DB_NAME}" -e "POSTGRES_USER=${JAWS_DB_USER}" -e "POSTGRES_PASSWORD=${JAWS_DB_PASSWORD}" -d "postgres:${JAWS_DB_IMAGE_VERSION}"
dstart: start-db

stop-db:
	docker stop "${JAWS_DB_CONTAINER_NAME}"
dstop: stop-db

clean-db-container: stop-db
	docker container rm "${JAWS_DB_CONTAINER_NAME}"
dcclean: clean-db-container
