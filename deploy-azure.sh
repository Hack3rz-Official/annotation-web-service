#!/bin/bash
set -x # echo commands
set -e # exit when any command fails
docker-compose -f docker-compose-azure.yml build
docker-compose -f docker-compose-azure.yml push
docker context use hack3rzcontext
docker compose -f docker-compose-azure.yml down
docker compose -f docker-compose-azure.yml up
docker context use default