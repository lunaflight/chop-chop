.PHONY: all check ci-check clear-cache-and-check fmt main accept-tests fix-all

all: main

main:
	@PYTHONPATH=$(shell pwd) python src/main.py $(args)

check:
	ruff check --no-fix
	ruff format --check
	mypy .
	pytest

ci-check:
	ruff check --no-fix --output-format=github .
	ruff format --check
	mypy .
	pytest

clear-cache-and-check:
	rm -f tests/scraper/cached_htmls/*.html
	$(MAKE) check

fmt:
	ruff format

fix-all:
	EXPECTTEST_ACCEPT=1 pytest
	ruff check --fix
	$(MAKE) fmt
