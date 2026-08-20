#!/usr/bin/env python3
"""Fetch GitHub pull request comments with review-thread state via gh."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any


QUERY = r"""
query($owner: String!, $repo: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      number
      url
      title
      state
      comments(first: 100) {
        nodes { id body createdAt updatedAt author { login } }
      }
      reviews(first: 100) {
        nodes { id state body submittedAt author { login } }
      }
      reviewThreads(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          startLine
          diffSide
          originalLine
          resolvedBy { login }
          comments(first: 100) {
            nodes { id body createdAt updatedAt author { login } url }
          }
        }
      }
    }
  }
}
"""


def run_gh(*args: str) -> str:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    result = subprocess.run(
        ["gh", *args],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
        env=env,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "gh command failed")
    return result.stdout


def resolve_context(repo: str | None, pr: int | None) -> tuple[str, str, int]:
    repository = repo or run_gh(
        "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"
    ).strip()
    if "/" not in repository:
        raise ValueError("Repository must use OWNER/REPO format")
    owner, name = repository.split("/", 1)
    number = pr or int(
        run_gh("pr", "view", "--json", "number", "--jq", ".number").strip()
    )
    return owner, name, number


def fetch(owner: str, repo: str, number: int) -> dict[str, Any]:
    cursor: str | None = None
    pull_request: dict[str, Any] | None = None
    threads: list[dict[str, Any]] = []

    while True:
        args = [
            "api",
            "graphql",
            "-f",
            f"query={QUERY}",
            "-f",
            f"owner={owner}",
            "-f",
            f"repo={repo}",
            "-F",
            f"number={number}",
        ]
        if cursor:
            args.extend(["-f", f"cursor={cursor}"])
        payload = json.loads(run_gh(*args))
        current = payload["data"]["repository"]["pullRequest"]
        if current is None:
            raise ValueError(f"Pull request #{number} was not found")
        if pull_request is None:
            pull_request = current
        page = current["reviewThreads"]
        threads.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]

    assert pull_request is not None
    return {
        "pull_request": {
            key: pull_request[key] for key in ("number", "url", "title", "state")
        },
        "conversation_comments": pull_request["comments"]["nodes"],
        "reviews": pull_request["reviews"]["nodes"],
        "review_threads": threads,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="GitHub repository as OWNER/REPO")
    parser.add_argument("--pr", type=int, help="Pull request number")
    args = parser.parse_args()
    try:
        owner, repo, number = resolve_context(args.repo, args.pr)
        print(json.dumps(fetch(owner, repo, number), ensure_ascii=False, indent=2))
        return 0
    except (RuntimeError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
