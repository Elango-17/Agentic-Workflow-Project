from tools.base import BaseTool
import requests
from typing import Optional, Dict, Any


class GitHubPRFetcher(BaseTool):
    """
    Tool to retrieve pull request data from a public GitHub repository.
    """

class GitHubPRFetcher(BaseTool):
    """
    Tool to retrieve pull request data from a public GitHub repository.
    """

    def execute(
        self,
        repo_owner: str,
        repo_name: str,
        max_prs: int = 10,
        state: str = "all",
    ) -> list:
        """
        Retrieve pull request data from a public GitHub repository.
        """

        if not repo_owner:
            raise ValueError("Repository owner is required")

        if not repo_name:
            raise ValueError("Repository name is required")

        if max_prs <= 0:
            raise ValueError(
                "max_prs must be greater than 0"
            )

        if state not in ["open", "closed", "all"]:
            raise ValueError(
                "state must be open, closed, or all"
            )

        # --------------------------------------------------
        # Validate inputs
        # --------------------------------------------------

        if max_prs <= 0:
            raise ValueError(
                "max_prs must be greater than 0"
            )

        if state not in ["open", "closed", "all"]:
            raise ValueError(
                "state must be open, closed, or all"
            )

        # --------------------------------------------------
        # GitHub API URL
        # --------------------------------------------------

        url = (
            f"https://api.github.com/repos/"
            f"{repo_owner}/{repo_name}/pulls"
        )

        # --------------------------------------------------
        # Request parameters
        # --------------------------------------------------

        params = {
            "state": state,
            "per_page": min(max_prs, 100),
        }

        # --------------------------------------------------
        # Headers
        # --------------------------------------------------

        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        # --------------------------------------------------
        # API request
        # --------------------------------------------------

        try:

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=30,
            )

            response.raise_for_status()

        except requests.exceptions.RequestException as exc:

            raise RuntimeError(
                f"Failed to fetch GitHub pull requests: {exc}"
            ) from exc

        # --------------------------------------------------
        # Process response
        # --------------------------------------------------

        prs = []

        for item in response.json():

            prs.append(
                {
                    "title": item.get("title", ""),
                    "number": item.get("number", 0),
                    "state": item.get("state", ""),
                    "created_at": item.get(
                        "created_at",
                        "",
                    ),
                    "updated_at": item.get(
                        "updated_at",
                        "",
                    ),
                    "author": item.get(
                        "user",
                        {},
                    ).get(
                        "login",
                        "",
                    ),
                    "url": item.get(
                        "html_url",
                        "",
                    ),
                }
            )

        return prs