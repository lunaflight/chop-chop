.PHONY: all check ci-check main

all: main

main:
	@PYTHONPATH=$(shell pwd) python src/main.py $(args)

check:
	ruff check
	mypy .
	pytest

ci-check:
	ruff check --output-format=github .
	mypy .
	pytest
