import os
import json
import uuid

from google.cloud import tasks_v2
from google import auth

from breezy import job_nimbus_service

TASKS_CLIENT = tasks_v2.CloudTasksClient()
_, PROJECT_ID = auth.default()

CLOUD_TASKS_PATH = (PROJECT_ID, "us-central1", "job-nimbus")
PARENT = TASKS_CLIENT.queue_path(*CLOUD_TASKS_PATH)


def create_tasks() -> dict:
    payloads = [
        {
            "name": f"{table}-{uuid.uuid4()}",
            "payload": {
                "table": table,
            },
        }
        for table in job_nimbus_service.services.keys()
    ]
    tasks = [
        {
            "name": TASKS_CLIENT.task_path(
                *CLOUD_TASKS_PATH,
                task=str(payload["name"]),
            ),
            "http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                "url": os.getenv("PUBLIC_URL"),
                "oidc_token": {
                    "service_account_email": os.getenv("GCP_SA"),
                },
                "headers": {
                    "Content-type": "application/json",
                },
                "body": json.dumps(payload["payload"]).encode(),
            },
        }
        for payload in payloads
    ]
    return {
        "tasks": len(
            [
                TASKS_CLIENT.create_task(
                    request={
                        "parent": PARENT,
                        "task": task,
                    }
                )
                for task in tasks
            ]
        ),
    }
