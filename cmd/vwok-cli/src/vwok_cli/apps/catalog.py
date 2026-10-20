from typing import Annotated

import typer

from vwok_cli.apps._helpers import get_client, run
from vwok_cli.apps._types import (
    BrandArgument,
    CountryArgument,
    LanguageOption,
    ProductDataKeyOption,
    TypeArgument,
)

app = typer.Typer(no_args_is_help=True)


@app.command()
def models(
    ctx: typer.Context,
    country_code: CountryArgument,
    brand: BrandArgument,
    language_code: LanguageOption = None,
    product_data_key: ProductDataKeyOption = None,
) -> None:
    """List the models of a brand."""
    run(
        get_client(ctx).list_models,
        country_code,
        brand,
        language_code=language_code,
        product_data_key=product_data_key,
    )


@app.command("base-configuration")
def base_configuration(
    ctx: typer.Context,
    country_code: CountryArgument,
    brand: BrandArgument,
    type_code: TypeArgument,
    language_code: LanguageOption = None,
    product_data_key: ProductDataKeyOption = None,
) -> None:
    """Get the default valid build for a type."""
    run(
        get_client(ctx).get_base_configuration,
        country_code,
        brand,
        type_code,
        language_code=language_code,
        product_data_key=product_data_key,
    )


@app.command()
def types(
    ctx: typer.Context,
    country_code: CountryArgument,
    model: Annotated[
        str, typer.Argument(help="Model id or code, e.g. MODEL:30100_31102")
    ],
    fetch_wltp_span: Annotated[
        bool | None, typer.Option(help="fetch_wltp_span")
    ] = None,
    language_code: LanguageOption = None,
    product_data_key: ProductDataKeyOption = None,
) -> None:
    """List the trims/engines of a model."""
    run(
        get_client(ctx).list_types,
        country_code,
        model,
        fetch_wltp_span=fetch_wltp_span,
        language_code=language_code,
        product_data_key=product_data_key,
    )


@app.command()
def options(
    ctx: typer.Context,
    country_code: CountryArgument,
    type_code: TypeArgument,
    language_code: LanguageOption = None,
    product_data_key: ProductDataKeyOption = None,
) -> None:
    """Get the option catalogue of a type."""
    run(
        get_client(ctx).get_type_options,
        country_code,
        type_code,
        language_code=language_code,
        product_data_key=product_data_key,
    )
