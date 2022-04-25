from breezy.job_nimbus_controller import job_nimbus_controller
from tasks.task_service import create_tasks


def main(request) -> dict:
    data: dict = request.get_json()
    print(data)

    if "table" in data:
        response = job_nimbus_controller(data["table"])
    elif "task" in data:
        response = create_tasks()
    else:
        raise ValueError(data)

    print(response)
    return response
