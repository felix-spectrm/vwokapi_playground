from typing import Any

import attrs


def to_dict(obj: Any) -> dict[str, Any]:
    """Recursively convert an attrs instance to a dict, omitting `None` fields."""
    return attrs.asdict(obj, filter=lambda _attr, value: value is not None)
