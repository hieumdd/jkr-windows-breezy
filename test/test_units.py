import pytest

from breezy.pipeline import pipelines
from breezy import breezy_repo, breezy_service


@pytest.fixture(
    params=pipelines.values(),
    ids=pipelines.keys(),
)
def pipeline(request):
    return request.param


class TestBreezy:
    def test_get_headers(self):
        assert breezy_repo.get_headers()

    def test_scrape_service(self, pipeline):
        res = breezy_service._scrape_service(pipeline)()
        assert res

    def test_pipeline_service(self, pipeline):
        res = breezy_service.pipeline_service(pipeline)
        assert res


# class TestTask:
#     def test_controller(self):
#         res = run({"task": "job-nimbus"})
#         assert res["tasks"] > 0
