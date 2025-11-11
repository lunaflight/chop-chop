This repository uses a Makefile to organise the useful development commands.

# Checks
Run `make check`. This encompasses style, static checking and tests.

For GitHub CI to work, the cached HTMLs must be committed.
This is because GitHub is unable to scrape the HTMLs by itself.

If you would like to purge the cached HTMLs and try again, run `make clear-cache-and-check`.

# Formatting
Run `make fmt`.
