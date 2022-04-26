from typing import Union, Any

from breezy.pipeline import pipelines
from breezy import breezy_service


def breezy_controller(body: dict[str, Any]) -> dict[str, Union[str, int]]:
    return breezy_service.pipeline_service(pipelines[body['table']])
