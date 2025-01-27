from typing import Any, Optional

import requests


class BaseAPI:
    def __init__(self, base_url: str, headers: dict[str, str]) -> None:
        self.base_url = base_url
        self.headers = headers

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
        files: Optional[dict[str, Any]] = None,
    ) -> Any:
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, params=params, json=json, files=files)
        response.raise_for_status()
        return response.json() if response.content else None
