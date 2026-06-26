#!/usr/bin/env python3
"""
Generate a repos.json file with information about github repositories with trame as topic.
Fetches: name, url, description, social preview image, and topics.
"""

import subprocess
import os
import json
import re
from jinja2 import Template


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
    query = (
        Template("""
        query {
        {%- for repo in repos %}
            {%- set owner = repo.split('/')[0] %}
            {%- set name = repo.split('/')[1] %}
            {%- set alias = repo.replace('/', '_').replace('-', '_') %}
            {{ alias }}: repository(owner: "{{ owner }}", name: "{{ name }}") {
                name
                nameWithOwner
                description
                openGraphImageUrl
                repositoryTopics(first: 10) {
                    nodes {
                        topic {
                            name
                        }
                    }
                }
                {%- for file in additional_files %}
                {{ file }}: object(expression: "HEAD:{{ additional_files[file] }}") {
                    ... on Blob {
                        text
                    }
                }
                {%- endfor %}
            }
            {%- endfor %}
        }
    """)
        .render(repos=repos, additional_files=additional_files)
        .strip()
    )
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
