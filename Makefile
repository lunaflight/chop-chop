.PHONY: all check ci-check fmt main

all: main

main:
	@PYTHONPATH=$(shell pwd) python src/main.py $(args)

check:
	ruff check
	ruff format --check
	mypy .
	pytest

ci-check:
	ruff check --output-format=github .
	ruff format --check
	mypy .
	pytest

fmt:
	ruff format

