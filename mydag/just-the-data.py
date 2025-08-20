#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [ "joblib" ]
# ///
"""
Data collection pipeline with joblib caching

Usage: uv run data_builder.py
"""
import typing

import joblib  # type: ignore[reportMissingTypeStubs,import-untyped]

T = typing.TypeVar("T")
memory = joblib.Memory(location=".cache", verbose=1)
Lines = typing.Iterable[str]


def cached(func: T) -> T:
    return memory.cache(func)  # type:ignore


GH_ORG = "getsentry"

del joblib  # hygiene


def run_command(*command: object) -> Lines:
    import shlex
    import sys

    command = tuple(str(arg) for arg in command)

    # set -o xtrace
    print(f"$ {shlex.join(command)}", file=sys.stderr)

    import subprocess

    proc = subprocess.Popen(command, stdout=subprocess.PIPE, encoding="UTF-8")
    assert proc.stdout, proc
    yield from proc.stdout

    if proc.wait() != 0:
        # set -o errexit -o pipefail
        raise SystemExit(proc.returncode)


def strip_lines(stdout: Lines) -> Lines:
    for line in stdout:
        line = line.strip()
        if line and not line.startswith("#"):
            yield line


def _get_git_emails(since: str) -> Lines:
    """Extract unique emails from git log."""
    # git log --pretty=format:"%H %ae %ce" --since "6 months ago"
    result = run_command("git", "log", f"--pretty=format:%H %ae %ce", "--since", since)

    for line in strip_lines(result):
        # Remove first 40 chars (commit hash), split remaining on spaces
        # This gives us author email and committer email
        parts = line[40:].strip().split()
        yield from parts


@cached
def get_git_emails(since: str = "6 months ago") -> Lines:
    return set(_get_git_emails(since))


def _get_github_team_slugs(org: str) -> Lines:
    """Get all team slugs for an organization."""
    yield from strip_lines(
        run_command("gh", "api", f"orgs/{org}/teams", "--paginate", "--jq", ".[].slug")
    )


@cached
def get_github_team_slugs(org: str) -> set[str]:
    return set(_get_github_team_slugs(org))


def _get_github_logins(org: str, team_slugs: Lines) -> Lines:
    """Get (non-unique) GitHub logins from all team members."""
    for slug in team_slugs:
        yield from strip_lines(
            run_command(
                "gh",
                "api",
                f"orgs/{org}/teams/{slug}/members",
                "--paginate",
                "--jq",
                ".[].login",
            )
        )


@cached
def get_github_logins(org: str, team_slugs: set[str]) -> set[str]:
    return set(_get_github_logins(org, team_slugs))


def write_data_files(emails: Lines, logins: Lines) -> tuple[list[str], list[str]]:
    """Write the collected data to files for compatibility with existing scripts."""
    emails = sorted(emails)
    with open("emails.list", "w") as f:
        for email in emails:
            f.write(f"{email}\n")

    logins = sorted(logins)
    with open("login.list", "w") as f:
        for login in logins:
            f.write(f"{login}\n")
    return emails, logins


def main() -> None:
    """Collect data and write files."""
    print("Collecting git emails...")
    emails = get_git_emails()
    team_slugs = get_github_team_slugs(GH_ORG)
    logins = get_github_logins(GH_ORG, team_slugs=team_slugs)

    print("Writing data files...")
    emails, logins = write_data_files(emails, logins)

    print(f"✓ emails.list: {len(emails)} entries")
    print(f"✓ login.list: {len(logins)} entries")


if __name__ == "__main__":
    main()
