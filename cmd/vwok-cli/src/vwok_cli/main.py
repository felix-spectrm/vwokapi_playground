import typer
import vwok_client

from vwok_cli.apps import catalog_app, operation_app
from vwok_cli.apps._types import BaseUrlOption, ClientIdOption, ClientSecretOption

app = typer.Typer(no_args_is_help=True)
app.add_typer(catalog_app, name="catalog", help="Read catalogue data.")
app.add_typer(operation_app, name="operation", help="Configure and validate builds.")


@app.callback()
def root(
    ctx: typer.Context,
    client_id: ClientIdOption = None,
    client_secret: ClientSecretOption = None,
    base_url: BaseUrlOption = vwok_client.DEFAULT_BASE_URL,
) -> None:
    """CLI for the VWOK API."""
    # Validated lazily in get_client so `--help` works without credentials.
    ctx.obj = (client_id, client_secret, base_url)
