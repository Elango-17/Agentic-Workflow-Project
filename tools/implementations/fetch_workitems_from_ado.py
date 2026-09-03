from tools.base import BaseTool

import requests
import base64

from typing import Optional, Dict, Any


class ADOWorkitemFetcher(BaseTool):
    """
    Tool to retrieve workitems from Azure DevOps (ADO) using REST API.
    """


    def execute(
        self,
        workitem_type: Optional[str] = None,
        query_parameters: Optional[Any] = None,
        include_relations: bool = False,
    ) -> Dict[str, Any]:

        personal_access_token = "<PAT>"
        organization_url = "<URL>"
        project_name = "<Project-Name>"

        if not personal_access_token:
            raise ValueError(
                "Personal access token is required"
            )

        if not project_name:
            raise ValueError(
                "Project name is required"
            )

        if not organization_url:
            raise ValueError(
                "Organization URL is required"
            )

        organization_url = organization_url.rstrip("/")

        # --------------------------------------------------
        # Authentication
        # --------------------------------------------------

        credentials = f":{personal_access_token}"

        encoded_credentials = base64.b64encode(
            credentials.encode()
        ).decode()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}",
        }

        # --------------------------------------------------
        # Step 1: Build WIQL query
        # --------------------------------------------------

        wiql_url = (
            f"{organization_url}/{project_name}"
            "/_apis/wit/wiql"
        )

        conditions = []

        if workitem_type:
            conditions.append(
                f"[System.WorkItemType] = '{workitem_type}'"
            )

        where_clause = ""

        if conditions:
            where_clause = (
                " WHERE " + " AND ".join(conditions)
            )

        wiql = (
            "SELECT [System.Id] "
            "FROM WorkItems"
            f"{where_clause} "
            "ORDER BY [System.Id]"
        )

        # --------------------------------------------------
        # Step 2: Execute WIQL query
        # --------------------------------------------------

        try:

            wiql_response = requests.post(
                wiql_url,
                headers=headers,
                json={
                    "query": wiql
                },
                params={
                    "api-version": "7.1"
                },
                timeout=30,
            )

            wiql_response.raise_for_status()

            wiql_result = wiql_response.json()

        except requests.exceptions.RequestException as exc:

            raise RuntimeError(
                f"Failed to execute Azure DevOps WIQL query: {exc}"
            ) from exc

        # --------------------------------------------------
        # Step 3: Extract work item IDs
        # --------------------------------------------------

        work_items = wiql_result.get(
            "workItems",
            []
        )

        if not work_items:

            return {
                "status": "success",
                "count": 0,
                "work_items": [],
            }

        work_item_ids = [
            item["id"]
            for item in work_items
        ]

        # --------------------------------------------------
        # Step 4: Fetch work item details
        # --------------------------------------------------

        workitems_url = (
            f"{organization_url}/{project_name}"
            "/_apis/wit/workitems"
        )

        params = {
            "ids": ",".join(
                map(str, work_item_ids[:200])
            ),
            "$expand": (
                "Relations"
                if include_relations
                else "None"
            ),
            "api-version": "7.1",
        }

        try:

            response = requests.get(
                workitems_url,
                headers=headers,
                params=params,
                timeout=30,
            )

            response.raise_for_status()

            result = response.json()

        except requests.exceptions.RequestException as exc:

            raise RuntimeError(
                f"Failed to fetch workitem details: {exc}"
            ) from exc

        # --------------------------------------------------
        # Step 5: Return structured result
        # --------------------------------------------------

        return {
            "status": "success",
            "count": len(
                result.get("value", [])
            ),
            "work_items": result.get(
                "value",
                []
            ),
        }