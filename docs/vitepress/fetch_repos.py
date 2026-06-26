#!/usr/bin/env python3
"""
Generate a repos.json file with information about github repositories with trame as topic.
Fetches: name, url, description, social preview image, and topics.
"""

import subprocess
import os
import json
import re


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


def retrieve_gh_repos_from_topic(topic: str):
    request = f"gh search repos --topic {topic} --limit 1000 --json fullName"
    result = json.loads(make_gh_request(request.split(" ")))
    result = [t["fullName"] for t in result]
    return result


def retrieve_multiple_repos_graphql(
    repos: list[str], additional_files: dict[str, str] = {}
):
    # Build the query parts
    repo_queries = []
    for repo in repos:
        owner, name = repo.split("/")
        alias = repo.replace("/", "_").replace("-", "_")
        files_queries = []
        for file_key, file_path in additional_files.items():
            files_queries.append(f"""
                {file_key}: object(expression: "HEAD:{file_path}") {{
                    ... on Blob {{
                        text
                    }}
                }}""")
        files_part = "\n".join(files_queries) if files_queries else ""
        repo_query = f"""
            {alias}: repository(owner: "{owner}", name: "{name}") {{
                name
                nameWithOwner
                description
                openGraphImageUrl
                repositoryTopics(first: 10) {{
                    nodes {{
                        topic {{
                            name
                        }}
                    }}
                }}
                {files_part}
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


def repos_to_json(repos, ignored_topics=[]):
    table = []
    for repo_data in repos.values():
        topics = []
        for node in repo_data["repositoryTopics"]["nodes"]:
            if node["topic"]["name"] not in ignored_topics:
                topics.append(node["topic"]["name"])
        url = f"https://github.com/{repo_data['nameWithOwner']}"

        table.append(
            {
                "name": repo_data["name"],
                "url": url,
                "description": repo_data["description"],
                "image": repo_data["openGraphImageUrl"],
                "topics": topics,
            }
        )
    return table


if __name__ == "__main__":
    repos = retrieve_gh_repos_from_topic("trame")
    repos_datas = retrieve_multiple_repos_graphql(repos)
    with open("repos.json", "w") as f:
        json.dump(repos_to_json(repos_datas, ["trame"]), f)
