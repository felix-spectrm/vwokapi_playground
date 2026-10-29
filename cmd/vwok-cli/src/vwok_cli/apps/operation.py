from typing import Annotated, Literal

import typer

from vwok_cli.apps._helpers import get_client, run
from vwok_cli.apps._types import (
    CountOption,
    CountryArgument,
    ExtendWithOption,
    IgnoreCategoryTypesOption,
    LanguageOption,
    NiceToHaveOption,
    PayloadArgument,
    PreferredOptionsOption,
    ProductDataKeyOption,
    RemoveOptionOption,
    SearchStrategyOption,
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


@app.command()
def images(
    ctx: typer.Context,
    country_code: CountryArgument,
    payload: PayloadArgument,
    image_format: Annotated[
        Literal["PNG", "JPG"] | None, typer.Option("--format", help="Image format")
    ] = None,
    width: Annotated[int | None, typer.Option(help="Audi and SEAT only")] = None,
    language_code: LanguageOption = None,
    product_data_key: ProductDataKeyOption = None,
) -> None:
    """List image links for a build (VW access needs separate approval)."""
    run(
        get_client(ctx).list_images,
        country_code,
        payload,
        image_format=image_format,
        width=width,
        language_code=language_code,
        product_data_key=product_data_key,
    )


@app.command()
def recover(
    ctx: typer.Context,
    country_code: CountryArgument,
    payload: PayloadArgument,
    language_code: LanguageOption = None,
    product_data_key: ProductDataKeyOption = None,
) -> None:
    """Drop conflicting options and return one buildable build."""
    run(
        get_client(ctx).recover,
        country_code,
        payload,
        language_code=language_code,
        product_data_key=product_data_key,
    )


@app.command()
def resolve(
    ctx: typer.Context,
    country_code: CountryArgument,
    payload: PayloadArgument,
    extended_order: bool | None = None,
    preferred_options: PreferredOptionsOption = None,
    nice_to_have: NiceToHaveOption = None,
    extend_with: ExtendWithOption = None,
    ignore_category_types: IgnoreCategoryTypesOption = None,
    search_strategy: SearchStrategyOption = None,
    language_code: LanguageOption = None,
    product_data_key: ProductDataKeyOption = None,
) -> None:
    """Complete a partial, buildable build so it becomes distinct."""
    run(
        get_client(ctx).resolve,
        country_code,
        payload,
        extended_order=extended_order,
        preferred_options=preferred_options,
        nice_to_have=nice_to_have,
        extend_with=extend_with,
        ignore_category_types=ignore_category_types,
        search_strategy=search_strategy,
        language_code=language_code,
        product_data_key=product_data_key,
    )


@app.command()
def solve(
    ctx: typer.Context,
    country_code: CountryArgument,
    payload: PayloadArgument,
    count: CountOption = None,
    remove_option: RemoveOptionOption = None,
    preferred_options: PreferredOptionsOption = None,
    nice_to_have: NiceToHaveOption = None,
    extend_with: ExtendWithOption = None,
    ignore_category_types: IgnoreCategoryTypesOption = None,
    stick_to_basetype: bool | None = None,
    stick_to_type: bool | None = None,
    allow_change_of_model: bool | None = None,
    force: bool | None = None,
    search_strategy: SearchStrategyOption = None,
    language_code: LanguageOption = None,
    product_data_key: ProductDataKeyOption = None,
) -> None:
    """Return up to --count complete alternative builds."""
    run(
        get_client(ctx).solve,
        country_code,
        payload,
        count=count,
        remove_option=remove_option,
        preferred_options=preferred_options,
        nice_to_have=nice_to_have,
        extend_with=extend_with,
        ignore_category_types=ignore_category_types,
        stick_to_basetype=stick_to_basetype,
        stick_to_type=stick_to_type,
        allow_change_of_model=allow_change_of_model,
        force=force,
        search_strategy=search_strategy,
        language_code=language_code,
        product_data_key=product_data_key,
    )


@app.command()
def solutions(
    ctx: typer.Context,
    country_code: CountryArgument,
    payload: PayloadArgument,
    count: CountOption = None,
    distinct: bool | None = None,
    remove_option: RemoveOptionOption = None,
    preferred_options: PreferredOptionsOption = None,
    nice_to_have: NiceToHaveOption = None,
    extend_with: ExtendWithOption = None,
    ignore_category_types: IgnoreCategoryTypesOption = None,
    allow_change_of_basetype: bool | None = None,
    allow_change_of_model: bool | None = None,
    stick_to_type: bool | None = None,
    force: bool | None = None,
    search_strategy: SearchStrategyOption = None,
    language_code: LanguageOption = None,
    product_data_key: ProductDataKeyOption = None,
) -> None:
    """Return ranked fixes (options to add and remove) for a broken build."""
    run(
        get_client(ctx).solutions,
        country_code,
        payload,
        count=count,
        distinct=distinct,
        remove_option=remove_option,
        preferred_options=preferred_options,
        nice_to_have=nice_to_have,
        extend_with=extend_with,
        ignore_category_types=ignore_category_types,
        allow_change_of_basetype=allow_change_of_basetype,
        allow_change_of_model=allow_change_of_model,
        stick_to_type=stick_to_type,
        force=force,
        search_strategy=search_strategy,
        language_code=language_code,
        product_data_key=product_data_key,
    )
