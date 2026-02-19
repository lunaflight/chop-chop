# Quick Start
Run `./scripts/lint.sh json_file [json_files...]` to run the script.

It runs a set of rules on the JSON files and catches mistakes to the best of
its ability. It does not guarantee that the JSON file is perfect.

To see all rules, run `./scripts/lint.sh --list`.

## Suppressing Rules
To set the level of severity, you may use the flag `--rule-level` with `all`,
`suggestion`, `warning`, `error`. This defaults to `suggestion`.

Since some files may flaunt the linter rules intentionally, suppressing the
rules is available through `--ignore-yaml yaml-file`. The yaml file is a list
of `trieId: [ rule code to ignore, rule code to ignore ... ]`

An example of a yaml file looks like this:

```yaml
lah: [ HBC, HWH, NRD, SII ]
what#3: [ hbc, sii ]
char siew pau: [ hbc ]
```

One may use the reserved word `ALL_` to suppress all rules like this:
```yaml
ALL_: [ LWA ]
```

## Providing a known word list
You may use the flag `--known-words` with a `.txt` file containing known words
separated by new lines. When checking if linked words such as in related fields
as well as inline hyperlinked words with `@{}`, it does a naive 1-for-1
membership check with the `.txt` file. For example, it naively checks if `what#3`,
`what` or `lah` exists in the `.txt` file.

This is somewhat of a hack and can be replaced easily with some other better
method if required, as the code is implemented with a generic
`Callable[[str], bool]` interface. As long as the function is implemented, it
will be able to check if something is a known word.
