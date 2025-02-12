from typing import Optional

import requests
from open_webui.retrieval.web.main import SearchResult


def search_bocha(
    url: str,
    api_key: str,
    locale: str,
    query: str,
    count: int,
    filter_list: Optional[list[str]] = None,
) -> list[SearchResult]:
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    response = requests.post(
        url,
        json={"query": query, "freshness": "noLimit", "count": count, "summary": True},
        headers=headers,
    )

    response.raise_for_status()

    json_response = response.json()
    raw_search_results = (
        json_response.get("data", {}).get("webPages", {}).get("value", []) or []
    )

    return [
        SearchResult(
            link=result.get("url"),
            title=result.get("name", ""),
            snippet=result.get("summary"),
        )
        for result in raw_search_results[:count]
    ]
