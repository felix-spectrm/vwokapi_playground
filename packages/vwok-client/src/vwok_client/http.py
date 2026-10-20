from dataclasses import dataclass
from typing import Any

import httpx

DEFAULT_BASE_URL = "https://example.invalid"


class ApiError(Exception):
    def __init__(self, status_code: int, body: str) -> None:
        super().__init__(f"HTTP {status_code}: {body}")
        self.status_code = status_code
        self.body = body


@dataclass
class VwokClient:
    token: str
    base_url: str = DEFAULT_BASE_URL

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
    ) -> Any:
        response = httpx.request(
            method,
            f"{self.base_url.rstrip('/')}/{path.lstrip('/')}",
            headers={"Authorization": f"Bearer {self.token}"},
            params=params,
            json=json,
            timeout=30.0,
        )
        if not response.is_success:
            raise ApiError(response.status_code, response.text)
        return response.json() if response.content else None
