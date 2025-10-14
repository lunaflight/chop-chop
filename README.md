# Credit Formatter
The aim of this repository is to provide an easy way to credit people online
for their linguistic attestations.

It employs Python and web scraping. Since we expect to query the website only
once for the information, web scraping is kept to a minimum, in a responsible
fashion.

# Installation
Ensure that you are using `Python 3.13`, but I suspect any sufficiently
modern version should work fine.

Clone this repository and do the following from the **project root** to avoid
relative path issues:

1. `python -m venv venv`
    - This sets up a virtual environment to manage project dependencies.

2. `source venv/bin/activate`
    - This activates the virtual environment.
    - To escape the environment, you can run `deactivate`.

3. `pip install -r requirements.txt`
    - This installs the required dependencies for the project.

4. `chmod +x src/main.py`
    - This step is optional, and only makes for easier execution.

5. `./src/main.py --help`
    - Run the script!

# Quick Start
Run `./src/main.py`.

The following table describes the list of supported platforms and notes on
how to obtain a URL for the platform.

| **Platform** | **Sample Link to Copy and Use** | **Notes** |
|--------------|----------|-----------|
| HardwareZone | https://forums.hardwarezone.com.sg/threads/any-good-use-for-myactivesg-credits.7163585/#post-157582701 | Hover the link icon on the comment and click the copy icon to obtain a direct link. |
| Reddit | https://www.reddit.com/r/singapore/comments/1o5i3fl/contract_for_marine_parade_free_shuttle_bus/nj9euqx/ | Click `permalink` on the comment to obtain a direct link. |
| SingaporeBrides | https://singaporebrides.com/weddingforum/threads/any-clubbers-out-there.1305/page-396#post-730029 | Hover the link icon on the comment and click the copy icon to obtain a direct link. |
| SingaporeMotherhood | https://singaporemotherhood.com/forum/threads/female-obgyn-recommendations.298237/post-8821891 | Hover the link icon on the comment and click the copy icon to obtain a direct link. |
