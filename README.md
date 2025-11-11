# Credit Formatter
The aim of this repository is to provide an easy way to credit people online
for their linguistic attestations.

It employs Python and web scraping. See below for the disclaimer on ethicality
of web scraping.

# Installation
Ensure that you are using `Python 3.13`, but I suspect any sufficiently
modern version should work fine.

`Python 3.10` and below will not work as it does not support some ISO date formats. 

Clone this repository and do the following from the **project root** to avoid
relative path issues:

## Linux / Unix
1. `python -m venv venv`
    - This sets up a virtual environment to manage project dependencies.

2. `source venv/bin/activate`
    - This activates the virtual environment.
    - To escape the environment, you can run `deactivate`.

3. `pip install -r requirements.txt`
    - This installs the required dependencies for the project.

5. `make args=--help`
    - Run the script. Note the `PYTHONPATH` environment variable to help it
    locate packages.
	
## Windows
### Automatic:
1. run `run.ps1` (right click and run with PowerShell).

### Manual (if script fails):
1. `python -m venv venv`
    - This sets up a virtual environment to manage project dependencies.

2. `venv\Scripts\Activate.ps1` (PowerShell) / `venv\Scripts\activate.bat` (Command Prompt)
    - This activates the virtual environment.
	- The prompt should change to something like: `(venv) C:\[path]`
    - To escape the environment, you can run `deactivate`.

3. `pip install -r requirements.txt`
    - This installs the required dependencies for the project.

5. `python -m src.main`
    - Run the script.

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
