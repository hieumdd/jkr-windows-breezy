from typing import Any, Optional
from functools import reduce
from datetime import datetime


def compose(*func):
    def _compose(f, g):
        return lambda x: f(g(x))

    return reduce(_compose, func, lambda x: x)


def transform_remove_mark(i: str) -> str:
    return i.replace('"', "")


def transform_null(i: str) -> Optional[str]:
    return transform_remove_mark(i) if i else None


def transform_date(i: Optional[str]) -> Optional[str]:
    return datetime.strptime(i, "%m/%d/%Y").isoformat(timespec="seconds") if i else None


def transform_datetime(i: Optional[str]) -> Optional[str]:
    return (
        datetime.strptime(i, "%m/%d/%Y %I:%M %p").isoformat(timespec="seconds")
        if i
        else None
    )


def transform_float(i: Optional[str]) -> Optional[float]:
    if i and i != "N/A":
        x = i.replace("$", "").replace(",", "")
        if "(" or ")" in x:
            x = x.replace("(", "-").replace(")", "")
        return round(float(x), 6)
    else:
        return None


def transform_boolean(i: Any) -> Optional[Any]:
    return i if i is not None else None
