from pathlib import Path

import yaml

from src.linter import rule

type T = dict[str, list[rule.T]]


def of_yaml(yaml_file_path: Path) -> T:
    with yaml_file_path.open(encoding="utf-8") as f:
        ignored_rules_data = yaml.safe_load(f)

    return {
        trie_id: [rule.of_code(code) for code in code_list]
        for trie_id, code_list in ignored_rules_data.items()
    }


def is_ignored(t: T, trie_id: str, rule_: rule.T) -> bool:
    return trie_id in t and rule_ in t[trie_id]


def create_from_dict(dict_: dict[str, list[rule.T]]) -> T:
    return dict_
