from typing import Any, Dict, Optional
import os
import re
import requests
from tools.base import BaseTool

class FetchGithubRepositoryStructure(BaseTool):
    """
    Tool to fetch the complete directory structure and metadata details for a public GitHub repository.
    """

    def _parse_github_url(self, repository_url: str) -> tuple[str, str]:
        """Extract owner and repo name from a GitHub repository URL."""
        clean_url = repository_url.rstrip("/")
        match = re.match(r"^https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?$", clean_url)
        if not match:
            raise ValueError(f"Invalid GitHub repository URL: {repository_url}")
        return match.group(1), match.group(2)

    def execute(self, repository_url: str, branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetches the complete directory structure and metadata details for a public GitHub repository.
        
        Args:
            repository_url: The full HTTPS URL of the public GitHub repository.
            branch: The specific branch to fetch the structure from. Defaults to default branch.
            
        Returns:
            A dictionary containing repository metadata, details, and the file tree.
        """
        if not repository_url or not isinstance(repository_url, str):
            raise ValueError("A valid 'repository_url' string is required.")

        owner, repo = self._parse_github_url(repository_url)

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Enterprise-Tool-FetchGithubRepositoryStructure"
        }

        # Optional GitHub Token for higher rate limits
        github_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if github_token:
            headers["Authorization"] = f"Bearer {github_token}"

        api_base = "https://api.github.com"

        try:
            # 1. Fetch repository metadata
            repo_resp = requests.get(f"{api_base}/repos/{owner}/{repo}", headers=headers, timeout=10)
            if repo_resp.status_code == 404:
                raise ValueError(f"Repository not found or is private: {owner}/{repo}")
            repo_resp.raise_for_status()
            repo_data = repo_resp.json()

            target_branch = branch if branch else repo_data.get("default_branch", "main")

            # 2. Fetch tree recursively
            tree_url = f"{api_base}/repos/{owner}/{repo}/git/trees/{target_branch}?recursive=1"
            tree_resp = requests.get(tree_url, headers=headers, timeout=15)
            if tree_resp.status_code == 404:
                raise ValueError(f"Branch not found: {target_branch}")
            tree_resp.raise_for_status()
            tree_data = tree_resp.json()

            return {
                "repository": {
                    "name": repo_data.get("name"),
                    "full_name": repo_data.get("full_name"),
                    "description": repo_data.get("description"),
                    "html_url": repo_data.get("html_url"),
                    "default_branch": repo_data.get("default_branch"),
                    "stargazers_count": repo_data.get("stargazers_count"),
                    "forks_count": repo_data.get("forks_count"),
                    "language": repo_data.get("language"),
                },
                "branch": target_branch,
                "truncated": tree_data.get("truncated", False),
                "tree": tree_data.get("tree", [])
            }

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Network or HTTP error occurred while communicating with GitHub API: {e}")
