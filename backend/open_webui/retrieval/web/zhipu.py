import logging
import uuid
from typing import Optional

import requests
from open_webui.env import SRC_LOG_LEVELS
from open_webui.retrieval.web.main import SearchResult

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])


def search_zhipu(
    url: str,
    api_key: str,
    locale: str,
    query: str,
    count: int,
    filter_list: Optional[list[str]] = None,
) -> list[SearchResult]:
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "tool": "web-search-pro",
            "request_id": str(uuid.uuid4()),
            "stream": False,
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ],
        }

        response = requests.post(url=url, headers=headers, json=payload)

        if response.status_code != 200:
            log.error(f"智谱搜索API返回错误: {response.status_code} - {response.text}")
            return []

        results = response.json()

        search_results = []
        choices = results.get("choices", [])
        for choice in choices:
            tool_calls = choice.get("message", {}).get("tool_calls", [])
            if len(tool_calls) > 0:
                search_result = tool_calls[-1].get("search_result", [])
                for r in search_result:
                    search_results.append(
                        SearchResult(
                            title=r.get("title", ""),
                            link=r.get("link", ""),
                            snippet=r.get("content", ""),
                            icon=r.get("icon", ""),
                            media=r.get("media", ""),
                        )
                    )

        return search_results[:count]

    except Exception as ex:
        log.error(f"智谱搜索出错: {ex}")
        raise ex
