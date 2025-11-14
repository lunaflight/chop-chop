.PHONY: all check ci-check clear-cache-and-check fmt main accept-tests fix-all

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

clear-cache-and-check:
	rm -f tests/scraper/cached_htmls/*.html
	$(MAKE) check

fmt:
	ruff format

accept-tests:
	EXPECTTEST_ACCEPT=1 pytest

fix-all:
	$(MAKE) accept-tests
	$(MAKE) fmt
