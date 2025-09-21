main:
		uv run main.py

lint:
		uvx ruff check

format: lint
		uv format
