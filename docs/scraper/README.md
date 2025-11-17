# Quick Start
Run `make` to run the script.

The following table describes the list of supported platforms and notes on
how to obtain a URL for the platform.

| **Platform** | **Examples** | **Sample Link to Copy and Use** | **Notes** |
|--------------|--------------|---------------------------------|-----------|
| Invision | Blowing Wind, Mycarforum | https://www.mycarforum.com/forums/topic/2111034-bringbuy-beer-from-sg-to-bintan-resorts/?do=findComment&comment=2114128 | Click on the 3 dots, then Share, then copy the link shown. |
| Reddit | Reddit | https://www.reddit.com/r/singapore/comments/1o5i3fl/contract_for_marine_parade_free_shuttle_bus/nj9euqx/ | Click `permalink` on the comment to obtain a direct link. |
| Xenforo | HardwareZone, SingaporeBrides, SingaporeMotherhood, S.O.F.T. | https://singaporemotherhood.com/forum/threads/female-obgyn-recommendations.298237/post-8821891 | Hover the link icon on the comment and click the copy icon to obtain a direct link. |

# Disclaimer on Web Scraping
For ethical reasons, the use of scraping in this repository is limited.

- The script must take a specific URL, and is not automatically crawled.
- The program only queries as much as or less than the number of queries made by
manually accessing the website through the browser.
- The tests which fetch HTMLs are cached locally, to ensure that the website are
not pummeled with requests every time a test is conducted.
