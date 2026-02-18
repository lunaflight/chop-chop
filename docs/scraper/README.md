# Quick Start
Run `./scripts/scrape.sh` to run the script.

The following table describes the list of supported platforms and notes on
how to obtain a URL for the platform.

| **Platform** | **Examples** | **Sample Link to Copy and Use** | **Notes** |
|--------------|--------------|---------------------------------|-----------|
| Invision | Blowing Wind, Mycarforum | https://www.mycarforum.com/forums/topic/2111034-bringbuy-beer-from-sg-to-bintan-resorts/?do=findComment&comment=2114128 | Click on the 3 dots, then Share, then copy the link shown. |
| Reddit | Reddit | https://www.reddit.com/r/singapore/comments/1o5i3fl/contract_for_marine_parade_free_shuttle_bus/nj9euqx/ | Click `permalink` on the comment to obtain a direct link. |
| RenoTalk | RenoTalk | https://www.renotalk.com/forum/topic/11895-housewarming-invite/page/588/?tab=comments#comment-304037 | Click the share button in the top-right corner. |
| Xenforo | BMW.SG, HardwareZone, SingaporeBrides, SingaporeMotherhood, S.O.F.T. | https://singaporemotherhood.com/forum/threads/female-obgyn-recommendations.298237/post-8821891 | Hover the link icon on the comment and click the copy icon to obtain a direct link. |

# HardwareZone Age Restriction
Around late 2025 / early 2026, HardwareZone introduced an age restriction on
certain posts, as outlined
[here](https://forums.hardwarezone.com.sg/help/minimum_age/).

To be able to scrape these posts, you must create an account on HardwareZone
and verify your identity via SingPass. Then, you need to provide your username
and password in `config/`. See the [README](../../README.md) in the root
directory for more details about initialising this.

To confirm the health of your script, run `inv check --clear-cache`, to ensure
that it attempts to re-fetch the age-restricted thread.

# Disclaimer on Web Scraping
For ethical reasons, the use of scraping in this repository is limited.

- The script must take a specific URL, and is not automatically crawled.
- The program only queries as much as or less than the number of queries made by
manually accessing the website through the browser.
- The tests which fetch HTMLs are cached locally, to ensure that the website are
not pummeled with requests every time a test is conducted.
