This repository uses a Makefile to organise the useful development commands.

# Checks
Run `make check`. This encompasses style, static checking and tests.

For GitHub CI to work, the cached HTMLs must be committed.
This is because GitHub is unable to scrape the HTMLs by itself.

If you would like to purge the cached HTMLs and try again, run `make
clear-cache-and-check`.

# Formatting
Run `make fmt`.

# Accepting Tests
This repository uses [expecttest](https://github.com/pytorch/expecttest), which
inlines the expected output in the file.

If there is a failing test, run `make accept-tests` to change the inlined
output to make it pass.
