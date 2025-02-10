.PHONY: help setup run test lint clean docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make setup      - Install dependencies"
	@echo "  make run       - Run Flask development server"
	@echo "  make test      - Run tests"
	@echo "  make lint      - Run code linting (flake8)"
	@echo "  make format    - Format code with black"
	@echo "  make clean     - Clean up python cache files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run app in Docker container"


setup:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

run:
	flask run

test:
	PYTHONPATH=$(PWD) pytest tests/ -v

lint:
	flake8 app/

format:
	black app/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +

docker-build:
	docker build -t flask-app .

docker-run:
	docker run -p 5000:5000 flask-app