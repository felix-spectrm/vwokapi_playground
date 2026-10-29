import json
from typing import Any, Literal

import cattrs
from attrs import define, field

from vwok_client.models._serialize import to_dict

SearchStrategy = Literal["Shortest", "Cheapest"]


@define
class Option:
    code: str


@define
class CustomConditionsOptions:
    one_of: list[list[Option]] | None = None
    none_of: list[Option] | None = None


@define
class CustomConditions:
    maximum_price: float | None = None
    minimum_price: float | None = None
    options: CustomConditionsOptions | None = None


@define
class Configuration:
    """Request body shared by `configure`, `check` and `marketing_code`."""

    model_code: str
    options: list[Option] = field(factory=list)
    brand_code: str | None = None
    custom_conditions: CustomConditions | None = None

    def to_body(self) -> dict[str, Any]:
        return to_dict(self)


class PayloadError(ValueError):
    """The payload is not valid JSON or does not match `Configuration`."""


def _structure_str(value: Any, _type: type) -> str:
    if not isinstance(value, str):
        raise TypeError(f"expected a string, got {type(value).__name__}")
    return value


_converter = cattrs.Converter(detailed_validation=True, forbid_extra_keys=True)
_converter.register_structure_hook(str, _structure_str)


def parse_configuration(raw: str) -> Configuration:
    try:
        return _converter.structure(json.loads(raw), Configuration)
    except json.JSONDecodeError as exc:
        raise PayloadError(f"invalid JSON: {exc}") from exc
    except cattrs.BaseValidationError as exc:
        raise PayloadError("\n".join(cattrs.transform_error(exc))) from exc
