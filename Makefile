# Basic Makefile for common developer tasks
.PHONY: install dev lint test gen-protos docker-build

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

dev:
	pip install -r requirements-dev.txt

lint:
	ruff check . || true

test:
	pytest -q

gen-protos:
	bash ./scripts/gen_protos.sh

docker-build:
	docker build -t cleo:latest .
