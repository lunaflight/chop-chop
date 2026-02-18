# This file exists because some posts require age verification to view.
# This was introduced around the start of 2026 / end of 2025.
# A post demonstrating an age restriction is as follows:
# https://forums.hardwarezone.com.sg/threads/whats-the-thread-that-have-all-the-scammers-faces-revealed-alon-with-their-name-and-summary.6938055/
# HWZ Forums quotes the following as a reason:
# https://forums.hardwarezone.com.sg/help/minimum_age/
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from config import credentials

USER_AGENT = UserAgent()
USER_AGENT_HEADER = {"User-Agent": USER_AGENT.random}
HARDWAREZONE_LOGIN_URL = "https://forums.hardwarezone.com.sg/login/login"


def get_session_cookie(
    credentials_: credentials.T,
) -> dict[str, str] | ValueError:
    username_and_password = credentials.get_hardwarezone_username_and_password(
        credentials_
    )
    if not username_and_password:
        return ValueError(
            "Error: Username and/or password not found in credentials."
        )
    username, password = username_and_password

    session = requests.Session()

    # An initial get is required to get some magic values required for
    # logging in.
    response = session.get(HARDWAREZONE_LOGIN_URL, headers=USER_AGENT_HEADER)
    soup = BeautifulSoup(response.text, "html.parser")
    xf_token_input = soup.find("input", {"name": "_xfToken"})
    if not xf_token_input:
        return ValueError(
            "Could not find input with _xfToken. The API has changed."
        )
    xf_token = xf_token_input["value"]

    xf_csrf = session.cookies.get("xf_csrf")
    xf_dbtech_security_session = session.cookies.get("xf_dbtechSecuritySession")
    cookies_header = {
        "Cookie": f"xf_dbtechSecuritySession={
            xf_dbtech_security_session
        }; xf_csrf={xf_csrf}"
    }

    login_data = {"login": username, "password": password, "_xfToken": xf_token}
    response = session.post(
        HARDWAREZONE_LOGIN_URL,
        headers=(cookies_header | USER_AGENT_HEADER),
        data=login_data,
    )

    xf_session = session.cookies.get("xf_session")
    if not xf_session:
        return ValueError("Could not retrieve xf_session token.")

    return {"xf_session": xf_session}
