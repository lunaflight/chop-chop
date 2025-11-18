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
