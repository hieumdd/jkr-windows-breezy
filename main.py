from breezy.breezy_controller import breezy_controller
from tasks.task_service import create_tasks


def main(request) -> dict:
    data: dict = request.get_json()
    print(data)

    if "table" in data:
        response = breezy_controller(data)
    elif "task" in data:
        response = create_tasks()
    else:
        raise ValueError(data)

    print(response)
    return response
