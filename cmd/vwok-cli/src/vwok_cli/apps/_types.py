from typing import Annotated

import typer
import vwok_client

from vwok_cli.apps._helpers import read_payload

ClientIdOption = Annotated[
    str | None, typer.Option(envvar="CLIENT_ID", help="OAuth client id")
]
ClientSecretOption = Annotated[
    str | None, typer.Option(envvar="CLIENT_SECRET", help="OAuth client secret")
]
BaseUrlOption = Annotated[str, typer.Option(envvar="BASE_URL", help="API base URL")]
LanguageOption = Annotated[str | None, typer.Option(help="language_code")]
ProductDataKeyOption = Annotated[str | None, typer.Option(help="product_data_key")]

CountryArgument = Annotated[str, typer.Argument(help="e.g. DE")]
BrandArgument = Annotated[str, typer.Argument(help="e.g. VW")]
TypeArgument = Annotated[str, typer.Argument(metavar="TYPE", help="e.g. TYPE:CT1CAM-…")]
PayloadArgument = Annotated[
    vwok_client.Configuration,
    typer.Argument(
        metavar="PAYLOAD",
        parser=read_payload,
        help="Configuration as JSON: inline, @file.json, or - for stdin",
    ),
]
