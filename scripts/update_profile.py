"""Refresh the checked-in public GitHub snapshot and its README images.

Run with Python 3.11+ and an authenticated gh CLI, or use --offline to render
the previously verified snapshot. Calendars are always read as a signed-out
visitor so private activity is displayed only to the extent shared publicly.
"""

import argparse
import json
import re
import subprocess
import time
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import Request, urlopen
from xml.etree import ElementTree

from render_profile import render_assets

LOGIN = "jamshid-muxsinov"
OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "stats"
ONE_DAY = timedelta(days=1)
REPOSITORIES = """
  repositories(privacy: PUBLIC, ownerAffiliations: [OWNER], first: 100, after: $cursor) {
    totalCount nodes { stargazerCount } pageInfo { endCursor hasNextPage }
  }
"""
OVERVIEW = """
query($login: String!, $prs: String!, $issues: String!, $cursor: String) {
  user(login: $login) {
    login createdAt
    repositoriesContributedTo(privacy: PUBLIC, includeUserRepositories: true, first: 1,
      contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) { totalCount }
    REPOSITORIES
  }
  prs: search(type: ISSUE, query: $prs) { issueCount }
  issues: search(type: ISSUE, query: $issues) { issueCount }
}
""".replace("REPOSITORIES", REPOSITORIES)
MORE_REPOS = ("query($login: String!, $cursor: String) { user(login: $login) {"
              + REPOSITORIES + "} }")


def nonnegative(value):
    if type(value) is not int or value < 0:
        raise ValueError("Missing or invalid GitHub count")
    return value


def api(endpoint, *flags, body=None):
    command = ["gh", "api", "--hostname", "github.com", endpoint, *flags]
    if body is not None:
        command.extend(["--input", "-"])
    result = subprocess.run(command, input=json.dumps(body) if body else None,
                            text=True, capture_output=True, timeout=60)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"GitHub API error on {endpoint}")
    payload = json.loads(result.stdout)
    if not isinstance(payload, dict) or "errors" in payload:
        raise ValueError(f"Incomplete GitHub response for {endpoint}")
    return payload


def graphql(query, **variables):
    return api("graphql", body={"query": query, "variables": variables})["data"]


def github_metrics(today):
    author = f"is:public author:{LOGIN}"
    data = graphql(OVERVIEW, login=LOGIN, prs=f"{author} is:pr", issues=f"{author} is:issue")
    user = data["user"]
    if user["login"] != LOGIN:
        raise ValueError("Unexpected GitHub account")

    repos = user["repositories"]
    expected = nonnegative(repos["totalCount"])
    stars = 0
    seen = 0
    cursors = set()
    while True:
        stars += sum(nonnegative(repo["stargazerCount"]) for repo in repos["nodes"])
        seen += len(repos["nodes"])
        if not repos["pageInfo"]["hasNextPage"]:
            break
        cursor = repos["pageInfo"]["endCursor"]
        if not cursor or cursor in cursors:
            raise ValueError("Invalid repository pagination")
        cursors.add(cursor)
        repos = graphql(MORE_REPOS, login=LOGIN, cursor=cursor)["user"]["repositories"]
    if seen != expected:
        raise ValueError("GitHub repository list changed during pagination")

    # Search counts public, indexed commits by their author date (default branches).
    search = api("search/commits", "-X", "GET", "-f",
                 f"q={author} author-date:{today.year}-01-01..{today}", "-F", "per_page=1")
    if search["incomplete_results"] is not False:
        raise ValueError("GitHub returned partial commit search results")
    metrics = {
        "stars": stars, "commits": nonnegative(search["total_count"]),
        "pull_requests": nonnegative(data["prs"]["issueCount"]),
        "issues": nonnegative(data["issues"]["issueCount"]),
        "repositories": nonnegative(user["repositoriesContributedTo"]["totalCount"]),
    }
    return date.fromisoformat(user["createdAt"][:10]), metrics


class CalendarParser(HTMLParser):
    """Join GitHub's accessible tooltip counts to its dated grid cells by ID."""

    def __init__(self):
        super().__init__()
        self.cells = {}
        self.tips = {}
        self.active = None
        self.buffer = []
        self.heading = ""
        self.profile = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "data-graph-url" in attrs:
            self.profile = attrs["data-graph-url"]
        if tag == "td" and "data-date" in attrs:
            key = attrs["id"]
            if key in self.cells:
                raise ValueError("Duplicate contribution cell")
            self.cells[key] = (attrs["data-date"], int(attrs["data-level"]))
        if tag == "h2" and attrs.get("id") == "js-contribution-activity-description":
            self.active, self.buffer = ("h2", None), []
        if tag == "tool-tip" and attrs.get("for", "").startswith("contribution-day-"):
            self.active, self.buffer = ("tool-tip", attrs["for"]), []

    def handle_data(self, data):
        if self.active:
            self.buffer.append(data)

    def handle_endtag(self, tag):
        if not self.active or self.active[0] != tag:
            return
        content = " ".join("".join(self.buffer).split())
        if tag == "h2":
            self.heading = content
        else:
            match = re.fullmatch(r"(No|[\d,]+) contributions? on .+\.?", content)
            if not match:
                raise ValueError("Unrecognized GitHub contribution tooltip")
            raw = match[1]
            self.tips[self.active[1]] = 0 if raw == "No" else int(raw.replace(",", ""))
        self.active = None

    def days(self, through):
        match = re.fullmatch(r"(No|[\d,]+) contributions? in (\d{4})", self.heading)
        if self.profile != f"/users/{LOGIN}/contributions" or not match or int(match[2]) != through.year:
            raise ValueError(f"Missing GitHub calendar for {through.year}")
        if self.cells.keys() != self.tips.keys():
            raise ValueError("Calendar cells do not match their tooltips")
        calendar = [{"date": day, "count": self.tips[key], "level": level}
                    for key, (day, level) in self.cells.items()]
        calendar.sort(key=lambda entry: entry["date"])
        total = 0 if match[1] == "No" else int(match[1].replace(",", ""))
        if sum(d["count"] for d in calendar) != total:
            raise ValueError("Calendar total disagrees with daily counts")
        # GitHub may include the rest of the calendar year in its response.
        days = [d for d in calendar if d["date"] <= str(through)]
        validate_days(days, through)
        return days


def validate_days(days, through):
    start = date(through.year, 1, 1)
    if len(days) != (through - start).days + 1:
        raise ValueError("Missing contribution dates")
    for offset, item in enumerate(days):
        count, level = nonnegative(item["count"]), nonnegative(item["level"])
        if item["date"] != str(start + offset * ONE_DAY) or level > 4 or bool(count) != bool(level):
            raise ValueError(f"Invalid contribution date, count or level: {item['date']}")


def read_calendar(through):
    url = (f"https://github.com/users/{LOGIN}/contributions"
           f"?from={through.year}-01-01&to={through}")
    request = Request(url, headers={"Accept-Language": "en", "User-Agent": "github-profile-readme"})
    with urlopen(request, timeout=40) as response:
        parser = CalendarParser()
        parser.feed(response.read().decode("utf-8"))
        parser.close()
    return parser.days(through)


def empty_streak():
    return {"days": 0, "start": None, "end": None}


def streaks(days, history, allow_today=True):
    run, longest = history["ending"], history["longest"]
    for index, item in enumerate(days):
        if item["count"]:
            run = {"days": run["days"] + 1, "start": run["start"] or item["date"], "end": item["date"]}
            if run["days"] > longest["days"]:
                longest = run
        elif index != len(days) - 1 or not allow_today:
            run = empty_streak()
    return {"current": run, "longest": longest}


def history_before_year(created, today, cached):
    through = date(today.year, 1, 1) - ONE_DAY
    if cached and cached["through"] == str(through):
        age = today - date.fromisoformat(cached["checked_on"])
        if timedelta(0) <= age < timedelta(days=7):
            return cached
    # Older years can change after GitHub recalculates a user's contributions.
    # Recheck them weekly, and immediately when the year rolls over.
    history = {"through": str(through), "checked_on": str(today),
               "ending": empty_streak(), "longest": empty_streak()}
    for year in range(created.year, today.year):
        result = streaks(read_calendar(date(year, 12, 31)), history, allow_today=False)
        history.update(ending=result["current"], longest=result["longest"])
    return history


def fetch(today, previous):
    created, metrics = github_metrics(today)
    history = history_before_year(created, today, previous.get("history"))
    days = read_calendar(today)
    metrics["contributions"] = sum(d["count"] for d in days)
    return {
        "login": LOGIN, "as_of": str(today), "start": f"{today.year}-01-01",
        "calendar_source": f"https://github.com/users/{LOGIN}/contributions",
        "metrics": metrics, "history": history, "streaks": streaks(days, history), "days": days,
    }


def summary(snapshot):
    metrics = snapshot["metrics"]
    login, start, end = snapshot["login"], snapshot["start"], snapshot["as_of"]
    calendar_url = f"https://github.com/{login}?tab=overview&from={start}&to={end}"
    rows = [
        ("Stars earned", metrics["stars"], "Stars on all public repositories owned by this account."),
        ("Public commits", metrics["commits"], f"Indexed commits attributed to the account on public default branches, by author date from {start} through {end}."),
        ("Pull requests", metrics["pull_requests"], "All public pull requests authored by the account, across all states."),
        ("Issues", metrics["issues"], "All public issues opened by the account, across all states."),
        ("Contributed repositories", metrics["repositories"], "Recent public repositories, including the account’s own, where GitHub records a commit, issue, pull request or repository creation."),
        ("Total contributions", metrics["contributions"], f"Sum of public profile calendar counts from {start} through {end}."),
    ]
    for key, label, scope in (
        ("current", "Current streak", "Consecutive active days ending today or yesterday."),
        ("longest", "Longest streak", "Longest run of active days across the account’s public calendar."),
    ):
        run = snapshot["streaks"][key]
        if run["days"]:
            period = run["start"] if run["days"] == 1 else f"{run['start']} through {run['end']}"
            scope = f"{scope.rstrip('.')} ({period})."
        unit = "day" if run["days"] == 1 else "days"
        rows.append((label, f"{run['days']} {unit}", scope))
    table = "\n".join(f"| {label} | {value} | {scope} |" for label, value, scope in rows)
    return (f"# Jamshid’s GitHub statistics\n\n"
            f"Public activity for **{login}**, updated **{end} UTC**.\n\n"
            f"| Metric | Value | Scope |\n| --- | ---: | --- |\n{table}\n\n"
            f"[GitHub contribution calendar]({calendar_url}) · "
            "[Snapshot with daily counts](snapshot.json)\n")


def write_snapshot(snapshot, output):
    through = date.fromisoformat(snapshot["as_of"])
    if snapshot["login"] != LOGIN or snapshot["start"] != f"{through.year}-01-01":
        raise ValueError("Unexpected snapshot account or period")
    validate_days(snapshot["days"], through)
    if sum(d["count"] for d in snapshot["days"]) != snapshot["metrics"]["contributions"]:
        raise ValueError("Snapshot contribution count mismatch")
    files = render_assets(snapshot)
    for source in files.values():
        root = ElementTree.fromstring(source)
        if root.tag != "{http://www.w3.org/2000/svg}svg" or len(root) < 3:
            raise ValueError("Empty or invalid statistics image")
    files["summary.md"] = summary(snapshot)
    files["snapshot.json"] = json.dumps(snapshot, indent=2) + "\n"
    # All network, parsing, rendering and serialization have succeeded before
    # replacing any output. The workflow commits the entire set together.
    with TemporaryDirectory(dir=output) as temp:
        stage = Path(temp)
        for name, source in files.items():
            (stage / name).write_text(source, encoding="utf-8")
        for name in files:
            (stage / name).replace(output / name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="render the checked-in snapshot")
    args = parser.parse_args()
    path = OUTPUT / "snapshot.json"
    previous = json.loads(path.read_text()) if path.exists() else {}
    if args.offline:
        if not previous:
            parser.error("Missing snapshot for offline rendering")
        snapshot = previous
    else:
        today = datetime.now(timezone.utc).date()
        for attempt in range(3):
            try:
                snapshot = fetch(today, previous)
                break
            except (OSError, RuntimeError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
                if attempt == 2:
                    raise SystemExit(f"Refresh failed. Previous images retained. {error}") from error
                time.sleep(2 ** (attempt + 1))
    write_snapshot(snapshot, OUTPUT)
    print(f"{snapshot['login']}: verified {len(snapshot['days'])} days through {snapshot['as_of']}")


if __name__ == "__main__":
    main()
