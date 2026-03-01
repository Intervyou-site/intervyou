# Makefile for ML Interview Coach Project

.PHONY: help install install-dev test train inference clean docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  train        - Run training pipeline"
	@echo "  inference    - Start inference server"
	@echo "  clean        - Clean cache and temporary files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run Docker container"

install:
	pip install -r requirements-prod.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	python -m pytest tests/ -v

train:
	python entrypoint/train.py

inference:
	python entrypoint/inference.py

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache

docker-build:
	docker build -t intervyou-ml .

docker-run:
	docker-compose up