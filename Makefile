#include .env

PROJECTNAME="Multistream"

build-docker:
	@docker build . -t multistream

run-docker:
	@echo "> Starting on port 1935"
	@docker run -p 1935:1935 -it multistream

bash-docker:
	@docker run -p 1935:1935 -it multistream bash

py-package:
	@python setup.py sdist

py-clean:
	@rm -rf ./__pycache__
	@rm -rf ./opa_test.egg-info

py-install:
	@pip install -r ./requirements.txt
	@pip install -e .

## build: Builds docker image
build: build-docker

## package: Builds compressed application artifact
package: py-package

## install: Installs app as CLI tool
install: py-install

## clean: Removes built files
clean: py-clean

## run: Runs application
run: run-docker

## help: Displays help text for make commands
.DEFAULT_GOAL := help
all: help
help: Makefile
	@echo " Choose a command run in "$(PROJECTNAME)":"
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'