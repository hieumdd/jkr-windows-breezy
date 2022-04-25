from unittest.mock import Mock

import pytest

from main import main

from breezy import job_nimbus, job_nimbus_service, repo
from utils.utils import compose


def run(data: dict) -> dict:
    return main(Mock(get_json=Mock(return_value=data), args=data))


@pytest.fixture(
    params=job_nimbus_service.services.values(),
    ids=job_nimbus_service.services.keys(),
)
def pipeline(request):
    return request.param


def read_data(file: str) -> bytes:
    with open(f"test/{file}.csv") as f:
        return f.read().encode("utf-8")


class TestScrape:
    def test_get_request(self):
        assert repo.get_request(None)

    def test_intercept(self):
        res = compose(
            repo.transform,
            repo.get_data,
            repo.get_request
        )(None)
        res


class TestPipeline:
    def test_load_service(self, pipeline: job_nimbus.Pipeline):
        assert (
            compose(
                job_nimbus_service._load_service(pipeline),
                repo.parse_content,
                read_data,
            )(pipeline.table)["output_rows"]
            > 0
        )

    def test_controller(self, pipeline: job_nimbus.Pipeline):
        assert run({"table": pipeline.table})


class TestTask:
    def test_controller(self):
        res = run({"task": "job-nimbus"})
        assert res["tasks"] > 0
