#!/usr/bin/env python3
"""
Generate a repos.json file with information about repositories both from repos of trusted github
owners with `trame` topic and from the `external_repos.yml` file.

Fetches: name, url, description, image, topics, stars, commit count, PR count, creation date, most
recent commit date, and whether it was created within the last year.

```mermaid
flowchart LR
    subgraph Wrapper [
        info contains: name, description, topics, image url, stars, last commit date, creation date,
        commits count, PRs count.
    ]
        direction LR
        A[external_repos.yml]
        B[GH repos in<br> trusted_owners<br> list with <br>`trame` topic]
        C((+))
        A -- "trusted <br>+= False" --> C
        B -- "trusted <br>= True" --> C
        C -- "url: {<br> trusted,<br> info<br>}" --> D((x))
        E[Fetch GH <br>for info]
        D -- GH url --> E
        D -- non GH url --> F((+))
        E --> F
        F -- "+is_new<br>if created<br>within last<br>year" --> G[repos.json]
    end

    style Wrapper fill:none,stroke:none
```
"""

import hashlib
import subprocess
import os
import json
import re
from datetime import datetime, timedelta, timezone
import requests
import time
import warnings
import yaml
from pathlib import Path

EXTERNAL_REPOS_FILE = "external_repos.yml"
OUTPUT_FILE = "repos.json"
IMAGES_DOWNLOAD_DIR = Path("public/repos_images")
IMAGES_SERVE_SUFFIX = "/trame/repos_images"


def github_action_formatwarning(message, category, filename, lineno, line=None):
    # Escape any colons or commas in the message
    safe_message = str(message).replace(":", "%3A").replace(",", "%2C")

    return f"::warning file={filename},line={lineno},title={category.__name__}::{safe_message}\n"


warnings.formatwarning = github_action_formatwarning


def extract_image_hash(url: str) -> str:
    """
    Extract a stable content identifier from GitHub's image-serving URLs, so
    that the same file is reused whenever the underlying content is unchanged
    and a new hash-derived filename is produced whenever it changes.

    Handles two known GitHub URL formats:
      - https://opengraph.githubassets.com/<hash>/owner/repo
        (dynamically rendered OG card; hash changes when repo metadata does)
      - https://repository-images.githubusercontent.com/<repo_id>/<uuid>
        (static, user-uploaded social preview image)

    For any other URL (no embedded content hash to rely on), the hash is
    salted with the current ISO week number, so the cached file is reused
    for up to a week and then naturally re-downloaded once the week rolls
    over, giving bounded staleness without needing explicit TTL/eviction
    logic.
    """
    match = re.search(
        r"opengraph\.githubassets\.com/([0-9a-f]{20,64})/([^/]+)/([^/?#]+)", url
    )
    if match:
        image_hash, owner, repo = match.groups()
        return f"{owner}-{repo}-{image_hash}"

    match = re.search(
        r"repository-images\.githubusercontent\.com/(\d+)/"
        r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
        url,
    )
    if match:
        repo_id, image_uuid = match.groups()
        return f"{repo_id}-{image_uuid}"

    year, week, _ = datetime.now(timezone.utc).isocalendar()
    weekly_prefix = f"{year}-W{week:02d}"
    url_hash = hashlib.sha256(url.encode()).hexdigest()
    return f"{weekly_prefix}-{url_hash}"


class ImageCacheMaker:
    """Downloads remote images to make the page serve them itself.

    Files are named after the hash embedded in the source URL, so unchanged
    repos resolve to the same filename run after run. Combined with a
    persisted cache directory (e.g. actions/cache), this means an image is
    only re-downloaded when its content actually changes.
    """

    def __init__(self, download_dir: Path, serve_url_suffix_base: str):
        """download_dir must be served at serve_url_suffix_base"""
        self._download_dir = download_dir
        self._download_dir.mkdir(parents=True, exist_ok=True)
        self._serve_url_suffix_base = serve_url_suffix_base
        self._used_files = set()

    def download(self, url: str):
        image_hash = extract_image_hash(url)
        filename = f"{image_hash}.png"
        local_path = self._download_dir / filename

        if local_path.exists():
            print(f"    Cache hit, skipping download: {filename}")
        else:
            download_remote_image(url, local_path)

        self._used_files.add(filename)
        return f"{self._serve_url_suffix_base}/{filename}"

    def prune_stale(self):
        """Remove cached images that are no longer referenced by any repo,
        so the cache doesn't grow unbounded as repos change over time."""
        if not self._download_dir.exists():
            return
        for existing in self._download_dir.iterdir():
            if existing.is_file() and existing.name not in self._used_files:
                print(f"    Pruning stale cached image: {existing.name}")
                existing.unlink()


def minify_graphql(query):
    query = re.sub(r"#.*$", "", query, flags=re.MULTILINE)
    query = re.sub(r"\s+", " ", query)
    for char in ["{", "}", "(", ")", ":", ","]:
        query = query.replace(f" {char}", char)
        query = query.replace(f"{char} ", char)
    query = query.strip()
    return query


def make_gh_request(request: list[str]):
    result = subprocess.run(request, capture_output=True, text=True, env=os.environ)
    if result.returncode != 0:
        raise Exception(
            f"Error executing command {' '.join(request)[:100]}:\n{result.stderr}\n{result.stdout}"
        )
    return result.stdout


def retrieve_gh_repos_from_topic(topic: str, owners: list = []):
    repos = {}
    for owner in owners:
        print(f"    Querying topic '{topic}' for owner '{owner}'...")
        request = [
            "gh",
            "search",
            "repos",
            "--topic",
            topic,
            "--owner",
            owner,
            "--limit",
            "1000",
            "--json",
            "url",
        ]
        result = json.loads(make_gh_request(request))
        for t in result:
            repos[t["url"]] = {"trusted": True}
        print(f"      Found {len(result)} repository/repositories for '{owner}'.")
    return repos


def download_remote_image(remote_url: str, local_path: str, max_retries: int = 5):
    for attempt in range(max_retries):
        response = requests.get(remote_url)

        if response.status_code == 200:
            with open(local_path, "wb") as file:
                file.write(response.content)
                print(f"    Saved {local_path}")
            return

        if response.status_code == 429:  # Too many requests
            retry_after = response.headers.get("Retry-After")
            wait = float(retry_after) if retry_after else (2**attempt)
            print(
                f"      Rate limited fetching {remote_url}, retrying in {wait:.1f}s "
                f"(attempt {attempt + 1}/{max_retries})..."
            )
            time.sleep(wait)
            continue

        raise Exception(
            f"Failed to download {remote_url}, status code: {response.status_code}"
        )

    raise Exception(
        f"Failed to download {remote_url} after {max_retries} retries (still rate limited)."
    )


def retrieve_repos_from_file(filename: str) -> list[str]:
    with open(filename, "r") as f:
        repos = yaml.safe_load(f)
        for repo_url, repo_info in repos.items():
            repo_info["trusted"] = repo_info.get("trusted", False)
        return repos


def retrieve_multiple_repos_graphql(repos: dict):
    repo_queries = []
    for repo_url, repo_info in repos.items():
        # Expecting format https://github.com/owner/name
        owner_name_part = repo_url.rstrip("/").split("github.com/")[-1]
        owner, name = owner_name_part.split("/")
        alias = re.sub(r"[^a-zA-Z0-9_]", "_", owner_name_part)
        repo_query = f"""
            {alias}: repository(owner: "{owner}", name: "{name}") {{
                name
                nameWithOwner
                description
                openGraphImageUrl
                createdAt
                stargazerCount
                repositoryTopics(first: 100) {{
                    nodes {{
                        topic {{
                            name
                        }}
                    }}
                }}
                pullRequests {{
                    totalCount
                }}
                defaultBranchRef {{
                    target {{
                        ... on Commit {{
                            history(first: 1) {{
                                totalCount
                                nodes {{
                                    committedDate
                                }}
                            }}
                        }}
                    }}
                }}
            }}"""
        repo_queries.append(repo_query)
    query = f"""
        query {{
            {",".join(repo_queries)}
        }}
    """.strip()
    mini_query = minify_graphql(query)
    cmd = ["gh", "api", "graphql", "-f", f"query={mini_query}"]
    data = {}
    attempt = 0
    while not data and attempt < 5:
        try:
            attempt += 1
            data = json.loads(make_gh_request(cmd))["data"]
        except Exception as e:
            warnings.warn(f"GraphQL request failed: {e}, attempt {attempt}/5.")
    if not data:
        return {}
    missing = [alias for alias, info in data.items() if info is None]
    for alias in missing:
        warnings.warn(f"Skipping missing repo: {alias} (not found on GitHub)")
    return {alias: info for alias, info in data.items() if info is not None}


def is_gh_url(url):
    return url.startswith("https://github.com/")


def repos_data_to_json(repos_data):
    fetched_repos = {}
    for repo_data in repos_data.values():
        topics = [
            node["topic"]["name"] for node in repo_data["repositoryTopics"]["nodes"]
        ]
        url = f"https://github.com/{repo_data['nameWithOwner']}"

        commit_count = 0
        last_commit_date = None
        if repo_data["defaultBranchRef"]:
            history = repo_data["defaultBranchRef"]["target"]["history"]
            commit_count = history["totalCount"]
            if history.get("nodes"):
                last_commit_date = history["nodes"][0]["committedDate"]
        else:
            warnings.warn(f"{url} has no default branch. Is it empty ?")
            continue

        fetched_repos[url] = {
            "name": repo_data["name"],
            "description": repo_data["description"] or "",
            "remoteImage": repo_data["openGraphImageUrl"],
            "topics": topics,
            "createdAt": repo_data["createdAt"],
            "lastCommitDate": last_commit_date,
            "stars": repo_data["stargazerCount"],
            "commitCount": commit_count,
            "pullRequestCount": repo_data["pullRequests"]["totalCount"],
        }
    return fetched_repos


def fetch_gh_info(gh_repos):
    fetched_repos_info = {}
    repos_data = retrieve_multiple_repos_graphql(gh_repos)
    json_repos_info = repos_data_to_json(repos_data)

    if not json_repos_info:
        return fetched_repos_info

    for url, repo_info in gh_repos.items():
        if url in json_repos_info:
            fetched_repos_info[url] = json_repos_info[url] | repo_info
        else:
            warnings.warn(
                f"The fetched github repository has a different URL than the one provided. Check "
                f"that the repository URL in `external_repos.yml` isn't an alias: {url}."
            )
    return fetched_repos_info


def add_info(repos):
    if not repos.items():
        return
    image_cache_maker = ImageCacheMaker(IMAGES_DOWNLOAD_DIR, IMAGES_SERVE_SUFFIX)
    one_year_ago = datetime.now(timezone.utc) - timedelta(days=365)
    for url, repo_info in repos.items():
        if not repo_info["trusted"]:
            repo_info["topics"].append("...")

        created_at = datetime.fromisoformat(
            repo_info["createdAt"].replace("Z", "+00:00")
        )
        repo_info["createdWithinLastYear"] = created_at >= one_year_ago

        repo_info["image"] = image_cache_maker.download(repo_info["remoteImage"])
    image_cache_maker.prune_stale()


if __name__ == "__main__":
    print("- Discovering trusted repositories from GitHub...")
    trusted_repos = retrieve_gh_repos_from_topic("trame", ["Kitware", "KitwareMedical"])

    print(f"- Loading external repositories from '{EXTERNAL_REPOS_FILE}'...")
    external_repos = retrieve_repos_from_file(EXTERNAL_REPOS_FILE)

    print("    Trusted repos:")
    for repo in trusted_repos:
        print(f"      {repo}")
    print("    External repos:")
    for repo in external_repos:
        print(f"      {repo}")

    repos = trusted_repos | external_repos

    gh_repos = {k: v for k, v in repos.items() if is_gh_url(k)}
    non_gh_repos = {k: v for k, v in repos.items() if not is_gh_url(k)}

    print(f"- Fetching GraphQL metadata for {len(gh_repos)} GitHub repositories...")
    fetched_gh_repos = fetch_gh_info(gh_repos)

    print(
        "- Enriching repository information, downloading images and calculating age..."
    )
    repos_w_info = non_gh_repos | fetched_gh_repos
    add_info(repos_w_info)

    print(f"- Writing combined results to '{OUTPUT_FILE}'...")
    with open(OUTPUT_FILE, "w") as f:
        json.dump(
            repos_w_info,
            f,
            sort_keys=True,
        )
    print("Done")
