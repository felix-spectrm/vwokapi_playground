import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, NoReturn

import typer
import vwok_client


def get_client(ctx: typer.Context) -> vwok_client.VwokClient:
    client_id, client_secret, base_url = ctx.obj
    if not client_id or not client_secret:
        raise typer.BadParameter(
            "--client-id and --client-secret (or CLIENT_ID / CLIENT_SECRET) are required"
        )
    return vwok_client.VwokClient.from_credentials(client_id, client_secret, base_url)


def read_payload(value: str) -> vwok_client.Configuration:
    try:
        if value == "-":
            raw = sys.stdin.read()
        elif value.startswith("@"):
            raw = Path(value[1:]).read_text()
        else:
            raw = value
        return vwok_client.parse_configuration(raw)
    except (OSError, vwok_client.PayloadError) as exc:
        raise typer.BadParameter(str(exc)) from exc


def fail_api_exception(exc: vwok_client.ApiError) -> NoReturn:
    typer.echo(f"HTTP {exc.status_code}: {exc.body}", err=True)
    if exc.correlation_id:
        typer.echo(f"x-okapi-correlation-id: {exc.correlation_id}", err=True)
    if exc.retry_after is not None:
        typer.echo(f"Retry-After: {exc.retry_after:g}s", err=True)
    raise typer.Exit(1) from exc


def run(call: Callable[..., object], *args: Any, **kwargs: Any) -> None:
    try:
        result = call(*args, **kwargs)
    except vwok_client.ApiError as exc:
        fail_api_exception(exc)
    except vwok_client.ResponseError as exc:
        typer.echo(f"Unexpected response shape:\n{exc}", err=True)
        raise typer.Exit(1) from exc
    typer.echo(json.dumps(vwok_client.to_dict(result), indent=2, ensure_ascii=False))
