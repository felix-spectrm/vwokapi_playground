import time
from typing import Any, Self

import httpx
from attrs import define, field

DEFAULT_BASE_URL = "https://api.productdata.volkswagenag.com"

_TOKEN_REFRESH_MARGIN = 60.0


class ApiError(Exception):
    """Non-2xx response. Covers gateway auth errors, OKAPI errors and 429s."""

    def __init__(
        self,
        status_code: int,
        body: str,
        *,
        error_code: str | None = None,
        correlation_id: str | None = None,
        retry_after: float | None = None,
    ) -> None:
        super().__init__(f"HTTP {status_code}: {body}")
        self.status_code = status_code
        self.body = body
        self.error_code = error_code
        self.correlation_id = correlation_id
        # Set on 429 (60 requests/minute per credential).
        self.retry_after = retry_after


def _error_code(response: httpx.Response) -> str | None:
    try:
        payload: Any = response.json()
    except ValueError:
        return None
    if isinstance(payload, dict):
        # OKAPI: {error_code, ...}; gateway auth: {error, ...}
        code: Any = payload.get("error_code") or payload.get("error")  # pyright: ignore[reportUnknownMemberType]
        return str(code) if code else None
    return None


def raise_for_error(response: httpx.Response) -> None:
    if response.is_success:
        return
    retry_after = response.headers.get("retry-after")
    raise ApiError(
        response.status_code,
        response.text,
        error_code=_error_code(response),
        correlation_id=response.headers.get("x-okapi-correlation-id"),
        retry_after=float(retry_after) if retry_after else None,
    )


def _encode_params(params: dict[str, Any]) -> dict[str, Any]:
    """Drop unset params and render bools the way OKAPI expects."""
    return {
        k: str(v).lower() if isinstance(v, bool) else v
        for k, v in params.items()
        if v is not None
    }


@define
class HttpClient:
    """Authenticated transport: OAuth client-credentials token + JSON requests."""

    client_id: str
    client_secret: str = field(repr=False)
    base_url: str = DEFAULT_BASE_URL
    transport: httpx.BaseTransport | None = field(
        default=None, kw_only=True, repr=False
    )
    _client: httpx.Client = field(init=False, repr=False)
    _token: str | None = field(default=None, init=False, repr=False)
    _expires_at: float = field(default=0.0, init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self._client = httpx.Client(
            base_url=self.base_url, timeout=30.0, transport=self.transport
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    def _access_token(self) -> str:
        if self._token is None or time.monotonic() >= self._expires_at:
            response = self._client.post(
                "/oauth2/token",
                auth=httpx.BasicAuth(self.client_id, self.client_secret),
                data={"grant_type": "client_credentials"},
            )
            raise_for_error(response)
            payload: dict[str, Any] = response.json()
            self._token = str(payload["access_token"])
            self._expires_at = (
                time.monotonic()
                + float(payload.get("expires_in", 3600))
                - _TOKEN_REFRESH_MARGIN
            )
        return self._token

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
    ) -> Any:
        response = self._client.request(
            method,
            path,
            headers={"Authorization": f"Bearer {self._access_token()}"},
            params=_encode_params(params or {}),
            json=json,
        )
        raise_for_error(response)
        return response.json() if response.content else None
