import json
from typing import Annotated, Any

import typer
from vwok_client import DEFAULT_BASE_URL, ApiError, VwokClient

app = typer.Typer(no_args_is_help=True)


@app.callback()
def root() -> None:
    """CLI for the VWOK API."""


TokenOption = Annotated[str, typer.Option(envvar="TOKEN", help="Bearer token")]
BaseUrlOption = Annotated[str, typer.Option(envvar="BASE_URL", help="API base URL")]


def print_response(data: Any) -> None:
    typer.echo(json.dumps(data, indent=2))


@app.command()
def request(
    method: str,
    path: str,
    token: TokenOption,
    base_url: BaseUrlOption = DEFAULT_BASE_URL,
    body: Annotated[str | None, typer.Option(help="Raw JSON request body")] = None,
) -> None:
    """Send a raw request, e.g. `vwok request GET /things`."""
    client = VwokClient(token=token, base_url=base_url)
    try:
        data = client.request(
            method.upper(), path, json=json.loads(body) if body else None
        )
    except ApiError as exc:
        typer.echo(f"{exc.status_code}: {exc.body}", err=True)
        raise typer.Exit(1) from exc
    print_response(data)
