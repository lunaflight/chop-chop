import json
from logging import getLogger
from pathlib import Path
from shutil import copy

CREDENTIALS_PATH = Path(__file__).parent / "credentials.json"
TEMPLATE_PATH = Path(__file__).parent / "credentials_template.json"

T = dict[str, str | None]


LOGGER = getLogger(__name__)


def create_credentials_from_template() -> None:
    copy(TEMPLATE_PATH, CREDENTIALS_PATH)
    LOGGER.info(
        "%s has been created from the template, since one does not exist.",
        CREDENTIALS_PATH,
    )


def get() -> T:
    if not Path(CREDENTIALS_PATH).exists():
        create_credentials_from_template()

    with Path(CREDENTIALS_PATH).open(encoding="utf-8") as file:
        return json.load(file)


def get_hardwarezone_username_and_password(t: T) -> tuple[str, str] | None:
    username = t.get("hardwarezone_username")
    password = t.get("hardwarezone_password")

    if username and password:
        return username, password

    return None
