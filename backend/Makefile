.PHONY: install test test-coverage lint format clean

install:
	pip install -r requirements.txt
	pip install -r requirements-test.txt

test:
	pytest tests/ -v --tb=short

test-coverage:
	pytest tests/ --cov=src --cov-report=html --cov-report=term

test-unit:
	pytest tests/ -m unit -v

test-integration:
	pytest tests/ -m integration -v

lint:
	ruff check src/ backend/ --fix

format:
	black src/ backend/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage

run-api:
	uvicorn main:app --reload --port 8000

run-tests-with-coverage:
	pytest tests/ --cov=src --cov-report=html:coverage_html --cov-report=term

view-coverage:
	open htmlcov/index.html  # macOS
	xdg-open htmlcov/index.html  # Linux
