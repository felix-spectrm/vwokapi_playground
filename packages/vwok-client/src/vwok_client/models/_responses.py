from typing import Any

import cattrs
from attrs import define, field


class ResponseError(ValueError):
    """The API response does not have the expected shape."""


@define
class Meta:
    count: int | None = None
    warnings: str | None = None


@define
class DataResponse[T]:
    data: list[T] = field(factory=list)
    meta: Meta | None = None


@define
class SalesClass:
    code: str
    description: str | None = None


@define
class Model:
    id: str
    code: str
    description: str | None = None
    language_code: str | None = None
    brand_code: str | None = None
    brand_description: str | None = None
    row_number: int | None = None
    sales_classes: list[SalesClass] = field(factory=list)


@define
class TypeModel:
    id: str
    code: str
    description: str | None = None
    price: float | None = None
    currency: str | None = None
    price_type: str | None = None
    basetype_code: str | None = None
    modelyear_code: str | None = None


@define
class OptionModel:
    code: str
    id: str | None = None
    category: str | None = None
    description: str | None = None
    price: float | None = None
    currency: str | None = None
    price_type: str | None = None
    is_selectable: bool | None = None
    is_standard: bool | None = None
    is_packet: bool | None = None
    row_number: int | None = None


@define
class BaseConfiguration:
    model_code: str
    brand_code: str | None = None
    options: list[OptionModel] = field(factory=list)


@define
class Category:
    id: str
    cardinality: str | None = None


@define
class TypeWithOptions:
    categories: list[Category] = field(factory=list)
    options: list[OptionModel] = field(factory=list)


@define
class Choice:
    id: str
    cardinality: str | None = None
    valid: list[OptionModel] = field(factory=list)
    invalid: list[OptionModel] = field(factory=list)


@define
class ImageLink:
    url: str
    key: str | None = None
    name: str | None = None


@define
class ConfigurationResult:
    """A build returned by `recover` and `resolve` (bare) and `solve` (in `data`)."""

    model_code: str | None = None
    brand_code: str | None = None
    model_description: str | None = None
    marketing_code: str | None = None
    options: list[OptionModel] = field(factory=list)


@define
class CodeDescription:
    code: str
    description: str | None = None


@define
class ConfigurationPrice:
    price: float | None = None
    currency: str | None = None
    price_type: str | None = None


@define
class Solution:
    add_options: list[OptionModel] = field(factory=list)
    remove_options: list[OptionModel] = field(factory=list)
    included_options: list[OptionModel] = field(factory=list)
    tags: list[str] = field(factory=list)
    configuration_price: ConfigurationPrice | None = None
    model: CodeDescription | None = None
    type: CodeDescription | None = None


@define
class CheckResponse:
    buildable: bool
    distinct: bool
    complete: bool


@define
class MarketingCodeConfiguration:
    marketing_code: str
    brand_code: str | None = None
    model_code: str | None = None
    options: list[OptionModel] = field(factory=list)


# Lenient on purpose: unknown fields in API responses are ignored.
_converter = cattrs.Converter(detailed_validation=True)


def parse_response[T](cls: type[T], raw: Any) -> T:
    try:
        return _converter.structure(raw, cls)
    except cattrs.BaseValidationError as exc:
        raise ResponseError("\n".join(cattrs.transform_error(exc))) from exc
