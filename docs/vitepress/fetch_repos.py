#!/usr/bin/env python3
"""
Generate a repos.json file with information about github repositories with trame
as topic.
Fetches: name, url, description, social preview image, topics, stars,
commit count, PR count, creation date, most recent commit date, and
whether it was created within the last year.
"""

import subprocess
import os
import json
import re
from datetime import datetime, timedelta, timezone


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
        raise Exception(f"Error: {result.stderr}")
    return result.stdout


def retrieve_gh_repos_from_topic(topic: str, owners: list = []):
    repos = []
    for owner in owners:
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
            "fullName",
        ]
        result = json.loads(make_gh_request(request))
        for t in result:
            repos.append(t["fullName"])
    return repos


def retrieve_gh_repos_from_file(filename: str) -> list[str]:
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]


def retrieve_multiple_repos_graphql(repos: list[str]):
    repo_queries = []
    for repo in repos:
        owner, name = repo.split("/")
        alias = repo.replace("/", "_").replace("-", "_")
        repo_query = f"""
            {alias}: repository(owner: "{owner}", name: "{name}") {{
                name
                nameWithOwner
                description
                openGraphImageUrl
                createdAt
                stargazerCount
                repositoryTopics(first: 10) {{
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
    data = json.loads(make_gh_request(cmd))["data"]
    return data


def repos_to_json(repos, ignored_topics=[], trusted_owners=[]):
    table = []
    one_year_ago = datetime.now(timezone.utc) - timedelta(days=365)
    for repo_data in repos.values():
        trustedOwner = repo_data["nameWithOwner"].split("/")[0] in trusted_owners
        topics = [] if trustedOwner else ["..."]
        for node in repo_data["repositoryTopics"]["nodes"]:
            if node["topic"]["name"] not in ignored_topics:
                topics.append(node["topic"]["name"])
        url = f"https://github.com/{repo_data['nameWithOwner']}"

        created_at = datetime.fromisoformat(
            repo_data["createdAt"].replace("Z", "+00:00")
        )
        created_within_last_year = created_at >= one_year_ago

        commit_count = 0
        last_commit_date = None
        if repo_data.get("defaultBranchRef"):
            history = repo_data["defaultBranchRef"]["target"]["history"]
            commit_count = history["totalCount"]
            if history.get("nodes"):
                last_commit_date = history["nodes"][0]["committedDate"]

        table.append(
            {
                "name": repo_data["name"],
                "url": url,
                "description": repo_data["description"],
                "image": repo_data["openGraphImageUrl"],
                "topics": topics,
                "trustedOwner": trustedOwner,
                "createdAt": repo_data["createdAt"],
                "createdWithinLastYear": created_within_last_year,
                "lastCommitDate": last_commit_date,
                "stars": repo_data["stargazerCount"],
                "commitCount": commit_count,
                "pullRequestCount": repo_data["pullRequests"]["totalCount"],
            }
        )
    return sorted(table, key=lambda r: r["name"].lower())


if __name__ == "__main__":
    repos = list(
        dict.fromkeys(
            retrieve_gh_repos_from_topic("trame", ["Kitware", "KitwareMedical"])
            + retrieve_gh_repos_from_file("external_gh_repos.txt")
        )
    )
    repos_datas = retrieve_multiple_repos_graphql(repos)
    with open("repos.json", "w") as f:
        json.dump(
            repos_to_json(repos_datas, ["trame"], ["Kitware", "KitwareMedical"]),
            f,
            sort_keys=True,
        )
