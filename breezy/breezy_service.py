from typing import Any, Union

from compose import compose

from breezy.pipeline.interface import Pipeline
from breezy import breezy_repo
from db.bigquery import load


def _scrape_service(pipeline: Pipeline) -> list[dict[str, Any]]:
    return compose(
        breezy_repo.get_api(pipeline.uri, pipeline.params_fn),
        breezy_repo.get_headers,
    )


def pipeline_service(pipeline: Pipeline) -> dict[str, Union[str, int]]:
    return compose(
        lambda x: {"table": pipeline.name, "output_rows": x},
        load(pipeline.name, pipeline.schema),
        pipeline.transform,
        _scrape_service(pipeline),
    )()
