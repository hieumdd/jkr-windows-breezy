from breezy.pipeline.interface import Pipeline
from breezy.pipeline.utils import current_year

pipeline = Pipeline(
    "Overview",
    "reports/overview",
    current_year,
    lambda res: [
        {
            "date": key,
            **value["data"],
        }
        for key, value in res["candidates"]["volume_history"].items()
    ],
    [
        {"name": "date", "type": "DATE"},
        {"name": "candidates", "type": "NUMERIC"},
        {"name": "views", "type": "NUMERIC"},
        {"name": "sourced", "type": "NUMERIC"},
        {"name": "referred", "type": "NUMERIC"},
        {"name": "recruited", "type": "NUMERIC"},
        {"name": "hired", "type": "NUMERIC"},
        {"name": "disqualified", "type": "NUMERIC"},
        {"name": "interviewed", "type": "NUMERIC"},
    ],
)
