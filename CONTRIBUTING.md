This repository uses [Invoke](https://github.com/pyinvoke/invoke) to organise
the useful development commands.
Run `inv --list` to see the list of available development commands.

# Checks
Run `inv check`. This encompasses style, static checking and tests.

For GitHub CI to work, the cached HTMLs must be committed.
This is because GitHub is unable to scrape the HTMLs by itself.

If you would like to purge the cached HTMLs and try again,
run `inv check --clear-cache`.

# Formatting
Run `inv fmt`.

# Accepting Tests
This repository uses [expecttest](https://github.com/pytorch/expecttest), which
inlines the expected output in the file.

If there is a failing test, run `inv fix` to change the inlined
output to make it pass.

# Adding new packages
Install the package you need with `pip install`.
Then, remember to run `pip freeze > requirements.txt` to update the
dependencies.
