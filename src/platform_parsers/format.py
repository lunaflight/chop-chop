from datetime import datetime

YYYY_MMM_D_FMT = "%Y %b %-d"


def online_with_title(timestamp: datetime,
                      name: str,
                      platform_name: str,
                      title: str,
                      url: str) -> str:
    return (f"{timestamp.strftime(YYYY_MMM_D_FMT)}, {name}. "
            f"{platform_name}, \"{title}\". {url}")
