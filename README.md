# Chop Chop Linguistic Compilation Tool
The aim of this repository is to provide tools for making compilation for the
[Chimbridge Singlish Dictionary](https://singlishdict.app/) easier.

It consists of some tools, which are outlined further below in this `README.md`
file.

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

# Credentials
You may wish to copy `config/credentials_template.json` to `config/credentials.json`,
containing various configuration details.
This file is not committed and should not be shared; `.gitignore` ensures that
`credentials.json` will not be committed.

# Tools
## Scraper
This tool helps scrape posts off the internet and format and credit the post in
a nice format conveniently.

See its [README](docs/scraper/README.md) for more details.

## Linter
This tool runs some rules against JSON files to check for mistakes automatically.

See its [README](docs/linter/README.md) for more details.
