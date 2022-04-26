from breezy.pipeline import pipelines
from tasks import cloud_tasks


def create_tasks_service(body) -> dict[str, int]:
    return {
        "tasks": cloud_tasks.create_tasks(
            [{"table": table} for table in pipelines.keys()],
            lambda x: x["table"],
        )
    }
