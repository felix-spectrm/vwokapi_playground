from typing import Annotated

import typer

from vwok_cli.apps._helpers import get_client, run
from vwok_cli.apps._types import (
    CountryArgument,
    LanguageOption,
    PayloadArgument,
    ProductDataKeyOption,
)

app = typer.Typer(no_args_is_help=True)


@app.command()
def configure(
    ctx: typer.Context,
    country_code: CountryArgument,
    payload: PayloadArgument,
    categories: Annotated[
        str | None, typer.Option(help="Option family, e.g. COLOR_EXTERIEUR")
    ] = None,
    with_add_dependencies: bool | None = None,
    with_remove_dependencies: bool | None = None,
    language_code: LanguageOption = None,
    product_data_key: ProductDataKeyOption = None,
) -> None:
    """List valid and invalid options for a build."""
    run(
        get_client(ctx).configure,
        country_code,
        payload,
        categories=categories,
        with_add_dependencies=with_add_dependencies,
        with_remove_dependencies=with_remove_dependencies,
        language_code=language_code,
        product_data_key=product_data_key,
    )


@app.command()
def check(
    ctx: typer.Context,
    country_code: CountryArgument,
    payload: PayloadArgument,
    complete: Annotated[
        bool | None, typer.Option(help="Also check completeness")
    ] = None,
    language_code: LanguageOption = None,
    product_data_key: ProductDataKeyOption = None,
) -> None:
    """Check whether a build is buildable, distinct and complete."""
    run(
        get_client(ctx).check,
        country_code,
        payload,
        complete=complete,
        language_code=language_code,
        product_data_key=product_data_key,
    )


@app.command("marketing-code")
def marketing_code(
    ctx: typer.Context,
    country_code: CountryArgument,
    payload: PayloadArgument,
    time_to_live: Annotated[str | None, typer.Option(help="time_to_live")] = None,
    language_code: LanguageOption = None,
    product_data_key: ProductDataKeyOption = None,
) -> None:
    """Save a build in VW's system and get a marketing code (a write)."""
    run(
        get_client(ctx).create_marketing_code,
        country_code,
        payload,
        time_to_live=time_to_live,
        language_code=language_code,
        product_data_key=product_data_key,
    )
