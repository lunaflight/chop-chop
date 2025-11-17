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

4. `chmod +x scripts/*.sh`
    - This ensures that the scripts are executable.
	
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

4. `python -m src.scraper.main`
    - Run the script.

# Tools
## Scraper
This tool helps scrape posts off the internet and format and credit the post in
a nice format conveniently.

See its [README](docs/scraper/README.md) for more details.

## Linter
This tool runs some rules against JSON files to check for mistakes automatically.

See its [README](docs/linter/README.md) for more details.
