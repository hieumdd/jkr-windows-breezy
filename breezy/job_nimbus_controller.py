from typing import Union

from breezy import job_nimbus_service


def job_nimbus_controller(table: str) -> dict[str, Union[str, int]]:
    return job_nimbus_service.pipeline_service(job_nimbus_service.services[table])
