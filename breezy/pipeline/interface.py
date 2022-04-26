from typing import Callable, Any
from dataclasses import dataclass


@dataclass
class Pipeline:
    name: str
    uri: str
    params_fn: Callable[[], dict[str, Any]]
    transform: Callable[[dict[str, Any]], list[dict[str, Any]]]
    schema: list[dict[str, Any]]
