from invoke import Context, task

from src.windows_hacks import AM_WINDOWS


def _run(c: Context, cmd: str) -> None:
    pty = not AM_WINDOWS
    c.run(cmd, pty=pty)  # pty=True is required for colour on Linux


def _pytest(c: Context, *, fix: bool) -> None:
    fix_env_var = "EXPECTTEST_ACCEPT=1" if fix else ""
    quiet_flag = "--quiet" if fix else ""
    cmd = f"{fix_env_var} pytest {quiet_flag}"
    _run(c, cmd)


def _ruff_check(c: Context, *, fix: bool, for_github: bool = False) -> None:
    fix_flag = "--fix" if fix else "--no-fix"
    output_flag = f"--output-format={'github' if for_github else 'full'}"
    cmd = f"ruff check {fix_flag} {output_flag}"
    _run(c, cmd)


def _ruff_format(c: Context, *, fix: bool) -> None:
    fix_flag = "" if fix else "--check"
    cmd = f"ruff format {fix_flag}"
    _run(c, cmd)


def _mypy(c: Context) -> None:
    _run(c, "mypy .")


@task
def check(
    c: Context, *, am_github: bool = False, clear_cache: bool = False
) -> None:
    if clear_cache:
        c.run("rm -f tests/scraper/cached_htmls/*.html")

    _ruff_check(c, fix=False, for_github=am_github)
    _ruff_format(c, fix=False)
    _mypy(c)
    _pytest(c, fix=False)


@task
def fix(c: Context) -> None:
    _ruff_check(c, fix=True)
    fmt(c)


@task
def fix_all(c: Context) -> None:
    _pytest(c, fix=True)
    _ruff_check(c, fix=True)
    fmt(c)


@task
def fmt(c: Context) -> None:
    _ruff_format(c, fix=True)
