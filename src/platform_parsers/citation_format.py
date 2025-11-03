from datetime import datetime

# Windows uses Microsoft strftime format, others use GNU strftime format
# only Windows uses \ in file path. thus this checks for windows or not
YYYY_MMM_D_FMT = "%Y %b %#d" if "\\" in __file__ else "%Y %b %-d"


def online_with_title(
    timestamp: datetime, name: str, platform_name: str, title: str, url: str
) -> str:
    return (
        f"{timestamp.strftime(YYYY_MMM_D_FMT)}, {name}. "
        f'{platform_name}, "{title}". {url}'
    )
