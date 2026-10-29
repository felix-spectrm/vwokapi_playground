from typing import Annotated, Literal

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

PreferredOptionsOption = Annotated[
    str | None,
    typer.Option(help="e.g. PACKET:G46+HET:3RC; used if they keep the build buildable"),
]
NiceToHaveOption = Annotated[
    str | None,
    typer.Option(help="e.g. PACKET:ZIE+PACKET:WBA; lower priority than the build"),
]
ExtendWithOption = Annotated[
    str | None, typer.Option(help="Domains to add, e.g. MARKET")
]
IgnoreCategoryTypesOption = Annotated[
    str | None, typer.Option(help="Only COLOR is accepted")
]
RemoveOptionOption = Annotated[str | None, typer.Option(help="Option to force-remove")]
SearchStrategyOption = Annotated[
    Literal["Shortest", "Cheapest"] | None,
    typer.Option(help="Fewest changes or lowest price (default Shortest)"),
]
CountOption = Annotated[int | None, typer.Option(min=1, help="Max results")]

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
