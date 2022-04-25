from typing import Callable
from dataclasses import dataclass

from db.bigquery import Schema


@dataclass
class Pipeline:
    url: str
    transform: Callable[[list[dict]], list[dict]]
    table: str
    schema: Schema
    update: bool
