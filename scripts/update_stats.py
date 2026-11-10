#!/usr/bin/env python3
"""Regenerate the live-stats block in the profile README.

Author: Diamond Rubinny
Uses only the Python standard library. Reads public data only.
Env:
  GITHUB_TOKEN  optional, raises the API rate limit
  GH_USER       GitHub username (default: diamondrubinny)
  README_PATH   path to README (default: README.md)
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

USER = os.environ.get("GH_USER", "diamondrubinny")
README = os.environ.get("README_PATH", "README.md")
API = "https://api.github.com"
START = "<!-- STATS:START -->"
END = "<!-- STATS:END -->"

# Repos shown in the table, in display order: (repo, label)
FEATURED: list[tuple[str, str]] = [
    ("Antirea", "🛡️ Antirea"),
    ("D.Ai", "🧠 D.Ai OS"),
    ("rubinny-signage", "📺 Rubinny Signage"),
    ("NexaHeart", "💜 NexaHeart"),
    ("keyflip", "⌨️ KeyFlip"),
    ("Botwa", "💬 Botwa"),
    ("Gameu", "🎮 Gameu"),
    ("menuai", "🍽️ MenuAI"),
    ("Scary", "🎃 SCARY"),
    ("TheIntegrator", "🔌 The Integrator"),
    ("PortZapper", "⚡ PortZapper"),
    ("Devguard", "🛡️ Devguard"),
    ("The-Horror-Archive", "🎬 The Horror Archive"),
]


def api_get(path: str):
    req = urllib.request.Request(f"{API}{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", f"{USER}-profile-stats")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return None
        raise


def fetch_repos() -> dict[str, dict]:
    repos: dict[str, dict] = {}
    page = 1
    while True:
        batch = api_get(f"/users/{USER}/repos?per_page=100&type=owner&page={page}") or []
        for r in batch:
            if not r.get("private") and not r.get("fork"):
                repos[r["name"]] = r
        if len(batch) < 100:
            return repos
        page += 1


def latest_release(name: str) -> str:
    rel = api_get(f"/repos/{USER}/{name}/releases?per_page=1")
    if not rel:
        return "—"
    tag = rel[0].get("tag_name", "")
    url = rel[0].get("html_url", f"https://github.com/{USER}/{name}/releases")
    return f"[{md_escape(tag)}]({url})" if tag else "—"


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")


def build_block(repos: dict[str, dict], followers: int, now: datetime) -> str:
    total_stars = sum(r.get("stargazers_count", 0) for r in repos.values())
    lines = [
        START,
        f"**{len(repos)}** public repositories · **{total_stars}** ⭐ total · "
        f"**{followers}** followers",
        "",
        "| Project | ⭐ Stars | Latest release | Last update |",
        "|---|:---:|---|---|",
    ]
    for name, label in FEATURED:
        r = repos.get(name)
        if not r:
            continue
        pushed = (r.get("pushed_at") or "")[:10] or "—"
        lines.append(
            f"| [{label}]({r['html_url']}) | {r.get('stargazers_count', 0)} | "
            f"{latest_release(name)} | {pushed} |"
        )
    lines += [
        "",
        f"<sub>Auto-updated daily by GitHub Actions · last run {now:%Y-%m-%d %H:%M} UTC</sub>",
        END,
    ]
    return "\n".join(lines)


def main() -> int:
    with open(README, encoding="utf-8") as fh:
        content = fh.read()
    if START not in content or END not in content:
        print("Stats markers not found in README", file=sys.stderr)
        return 1

    repos = fetch_repos()
    user = api_get(f"/users/{USER}") or {}
    block = build_block(repos, int(user.get("followers", 0)), datetime.now(timezone.utc))

    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    updated = pattern.sub(lambda _m: block, content, count=1)

    # Ignore the timestamp line when deciding whether anything really changed
    def strip_ts(s: str) -> str:
        return re.sub(r"last run [0-9:\- ]+UTC", "", s)

    if strip_ts(updated) == strip_ts(content):
        print("No changes")
        return 0
    with open(README, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(updated)
    print("README updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
