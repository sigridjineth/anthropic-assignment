.PHONY: install run dev test lint format clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run the application"
	@echo "  make dev        - Run with auto-reload (development)"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linter"
	@echo "  make format     - Format code"
	@echo "  make clean      - Clean cache files"
	@echo "  make env        - Create .env from example"

# Install dependencies
install:
	uv sync

# Run the application
run:
	uv run uvicorn src.main:app --host 0.0.0.0 --port 8000

# Run with auto-reload (development)
dev:
	uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	uv run pytest tests/ -v

# Run linter
lint:
	uv run ruff check src/ tests/

# Format code
format:
	uv run ruff format src/ tests/

# Clean cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage htmlcov/

# Create .env from example
env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env from .env.example"; \
		echo "Please edit .env and add your ANTHROPIC_API_KEY"; \
	else \
		echo ".env already exists"; \
	fi
